# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import tempfile
from collections import Counter
from typing import List, Optional, Tuple, Union
import numpy as np
import onnx
import onnxruntime as ort
from digest.model_class.digest_model import (
    NodeTypeCounts,
    NodeData,
    NodeShapeCounts,
    TensorData,
    TensorInfo,
)


# Convert tensor type to human-readable string and size in bytes
def tensor_type_to_str_and_size(elem_type) -> Tuple[str, int]:
    # Mapping of ONNX's data types to Python data types and their byte sizes
    type_mapping = {
        1: ("float32", 4),
        2: ("uint8", 1),
        3: ("int8", 1),
        4: ("uint16", 2),
        5: ("int16", 2),
        6: ("int32", 4),
        7: ("int64", 8),
        8: ("string", 0),  # Variable size
        9: ("bool", 1),
        10: ("float16", 2),
        11: ("double", 8),
        12: ("uint32", 4),
        13: ("uint64", 8),
        14: ("complex64", 8),  # Comprises two 32-bit floats
        15: ("complex128", 16),  # Comprises two 64-bit floats
        16: ("bfloat16", 2),
    }

    return type_mapping.get(elem_type, ("unknown", 0))


def load_onnx(onnx_path: str, load_external_data: bool = True) -> onnx.ModelProto:
    if os.path.exists(onnx_path):
        return onnx.load(onnx_path, load_external_data=load_external_data)
    else:
        raise ValueError(f"ONNX file {onnx_path} does not exist.")


def get_opset(model: onnx.ModelProto) -> Union[None, int]:
    for import_ in model.opset_import:
        if import_.domain == "" or import_.domain == "ai.onnx":
            return import_.version
    return None


def get_parameter_count(model: onnx.ModelProto) -> int:
    # Initialize parameter count
    total_parameters = np.int64(0)

    # Loop through all initializers (which are the parameters of the model)
    for initializer in model.graph.initializer:
        # Initializers contain the parameter values
        # so you can count them by getting the size of the initializer tensor
        param_count = np.prod(np.array(initializer.dims))
        total_parameters += param_count

    return int(total_parameters)


def get_node_type_counts(model: onnx.ModelProto) -> NodeTypeCounts:
    ops_counter: Counter = Counter()
    for node in model.graph.node:
        ops_counter[node.op_type] += 1
    node_type_counts = NodeTypeCounts(ops_counter.most_common())
    return node_type_counts


def get_node_shape_counts(node_data: NodeData) -> NodeShapeCounts:
    tensor_shape_counter = NodeShapeCounts()
    for _, info in node_data.items():
        shape_hash = tuple([tuple(v.shape) for _, v in info.inputs.items()])
        if info.node_type:
            tensor_shape_counter[info.node_type][shape_hash] += 1
    return tensor_shape_counter


def attribute_to_dict(attribute):
    """
    Helper function that returns a dictionary containing node attributes
    """
    attribute_dict = {}
    for field in ["f", "i", "s"]:
        if attribute.HasField(field):
            attribute_dict[attribute.name] = getattr(attribute, field)
            return attribute_dict
    if attribute.ints:
        attribute_dict[attribute.name] = list(attribute.ints)
    elif attribute.floats:
        attribute_dict[attribute.name] = list(attribute.floats)
    elif attribute.strings:
        attribute_dict[attribute.name] = list(attribute.strings)
    else:
        attribute_dict[attribute.name] = "unknown_type"
    return attribute_dict


def get_dynamic_input_dims(onnx_model: onnx.ModelProto) -> List[str]:
    dynamic_input_dim_names = []
    for tensor in onnx_model.graph.input:
        for dim in tensor.type.tensor_type.shape.dim:
            if dim.dim_param and dim.dim_param not in dynamic_input_dim_names:
                dynamic_input_dim_names.append(dim.dim_param)
    return dynamic_input_dim_names


def get_model_input_shapes_types(onnx_model: onnx.ModelProto):
    input_shapes_types = TensorData()
    for tensor in onnx_model.graph.input:
        input_shapes_types[tensor.name] = TensorInfo()
        tensor_shape: List[Union[str, int]] = []
        for dim in tensor.type.tensor_type.shape.dim:
            if dim.dim_value:
                tensor_shape.append(dim.dim_value)
            else:
                tensor_shape.append(dim.dim_param)

        type_str, type_byte_size = tensor_type_to_str_and_size(
            tensor.type.tensor_type.elem_type
        )

        size_kbytes = None
        if all(isinstance(s, int) for s in tensor_shape) and type_byte_size:
            tensor_size = float(np.prod(np.array(tensor_shape)))
            size_kbytes = tensor_size * float(type_byte_size) / 1024.0

        input_shapes_types[tensor.name].dtype = type_str
        input_shapes_types[tensor.name].dtype_bytes = type_byte_size
        input_shapes_types[tensor.name].shape = tensor_shape
        input_shapes_types[tensor.name].size_kbytes = size_kbytes

    return input_shapes_types


def get_model_output_shapes_types(onnx_model: onnx.ModelProto):
    output_shapes_types = TensorData()
    for tensor in onnx_model.graph.output:
        output_shapes_types[tensor.name] = TensorInfo()
        tensor_shape: List[Union[str, int]] = []
        for dim in tensor.type.tensor_type.shape.dim:
            if dim.dim_value:
                tensor_shape.append(dim.dim_value)
            else:
                tensor_shape.append(dim.dim_param)

        type_str, type_byte_size = tensor_type_to_str_and_size(
            tensor.type.tensor_type.elem_type
        )

        size_kbytes = None
        if all(isinstance(s, int) for s in tensor_shape) and type_byte_size:
            tensor_size = float(np.prod(np.array(tensor_shape)))
            size_kbytes = tensor_size * float(type_byte_size) / 1024.0

        output_shapes_types[tensor.name].dtype = type_str
        output_shapes_types[tensor.name].dtype_bytes = type_byte_size
        output_shapes_types[tensor.name].shape = tensor_shape
        output_shapes_types[tensor.name].size_kbytes = size_kbytes

    return output_shapes_types


def optimize_onnx_model(
    model_proto: onnx.ModelProto,
    model_filepath: Optional[str] = None,
    optimization_level=ort.GraphOptimizationLevel.ORT_ENABLE_BASIC,
) -> Tuple[onnx.ModelProto, bool]:

    # Attempt to optimize the model using onnxruntime.
    # In many cases, the model may not be capable of optimizations because
    # it may contain a custom operator that isn't recognized by onnxruntime, or
    # it could be due to digest not loading external data. These can be
    # included as future features.

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            sess_options = ort.SessionOptions()
            sess_options.graph_optimization_level = optimization_level
            sess_options.optimized_model_filepath = str(
                os.path.join(tmpdir, "opt.onnx")
            )
            _ = ort.InferenceSession(
                model_filepath if model_filepath else model_proto.SerializeToString(),
                sess_options,
                providers=["CPUExecutionProvider"],
            )
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error loading model into inference session: {e}")
            return model_proto, False

        try:
            onnx.checker.check_model(
                sess_options.optimized_model_filepath, full_check=True
            )
            model_proto = load_onnx(
                sess_options.optimized_model_filepath, load_external_data=False
            )
            return model_proto, True

        except onnx.checker.ValidationError:
            print("Model did not pass checker!")
            return model_proto, False


def get_supported_opset() -> int:
    """This function will return the opset version associated
    with the currently installed ONNX library"""
    return onnx.defs.onnx_opset_version()
