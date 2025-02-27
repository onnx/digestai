# Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.

import os
from typing import List, Dict, Optional, Tuple, cast
from datetime import datetime
import importlib.metadata
from collections import OrderedDict
import yaml
import numpy as np
import onnx
from prettytable import PrettyTable
from digest.model_class.digest_model import (
    DigestModel,
    SupportedModelTypes,
    NodeInfo,
    TensorData,
    TensorInfo,
)
import utils.onnx_utils as onnx_utils


class DigestOnnxModel(DigestModel):
    def __init__(
        self,
        onnx_model: onnx.ModelProto,
        onnx_filepath: str = "",
        model_name: str = "",
        save_proto: bool = True,
    ) -> None:
        super().__init__(onnx_filepath, model_name, SupportedModelTypes.ONNX)

        self.model_type = SupportedModelTypes.ONNX

        # Public members exposed to the API
        self.model_proto: Optional[onnx.ModelProto] = onnx_model if save_proto else None
        self.model_version: Optional[int] = None
        self.graph_name: Optional[str] = None
        self.producer_name: Optional[str] = None
        self.producer_version: Optional[str] = None
        self.ir_version: Optional[int] = None
        self.opset: Optional[int] = None
        self.imports: OrderedDict[str, int] = OrderedDict()

        # Private members not intended to be exposed
        self.input_tensors_: Dict[str, onnx.ValueInfoProto] = {}
        self.output_tensors_: Dict[str, onnx.ValueInfoProto] = {}
        self.value_tensors_: Dict[str, onnx.ValueInfoProto] = {}
        self.init_tensors_: Dict[str, onnx.TensorProto] = {}

        self.update_state(onnx_model)

    def update_state(self, model_proto: onnx.ModelProto) -> None:
        self.model_version = model_proto.model_version
        self.graph_name = model_proto.graph.name
        self.producer_name = model_proto.producer_name
        self.producer_version = model_proto.producer_version
        self.ir_version = model_proto.ir_version
        self.opset = onnx_utils.get_opset(model_proto)
        self.imports = OrderedDict(
            sorted(
                (import_.domain, import_.version)
                for import_ in model_proto.opset_import
            )
        )

        self.model_inputs = onnx_utils.get_model_input_shapes_types(model_proto)
        self.model_outputs = onnx_utils.get_model_output_shapes_types(model_proto)

        self.node_type_counts = onnx_utils.get_node_type_counts(model_proto)
        self.parse_model_nodes(model_proto)

    def get_node_tensor_info_(
        self, onnx_node: onnx.NodeProto
    ) -> Tuple[TensorData, TensorData]:
        """
        This function is set to private because it is not intended to be used
        outside of the DigestOnnxModel class.
        """

        input_tensor_info = TensorData()
        for node_input in onnx_node.input:
            input_tensor_info[node_input] = TensorInfo()
            if (
                node_input in self.input_tensors_
                or node_input in self.value_tensors_
                or node_input in self.output_tensors_
            ):
                tensor = (
                    self.input_tensors_.get(node_input)
                    or self.value_tensors_.get(node_input)
                    or self.output_tensors_.get(node_input)
                )
                if tensor:
                    for dim in tensor.type.tensor_type.shape.dim:
                        if dim.HasField("dim_value"):
                            input_tensor_info[node_input].shape.append(dim.dim_value)
                        elif dim.HasField("dim_param"):
                            input_tensor_info[node_input].shape.append(dim.dim_param)

                    dtype_str, dtype_bytes = onnx_utils.tensor_type_to_str_and_size(
                        tensor.type.tensor_type.elem_type
                    )
            elif node_input in self.init_tensors_:
                input_tensor_info[node_input].shape.extend(
                    [dim for dim in self.init_tensors_[node_input].dims]
                )
                dtype_str, dtype_bytes = onnx_utils.tensor_type_to_str_and_size(
                    self.init_tensors_[node_input].data_type
                )
            else:
                dtype_str = None
                dtype_bytes = None

            input_tensor_info[node_input].dtype = dtype_str
            input_tensor_info[node_input].dtype_bytes = dtype_bytes

            if (
                all(isinstance(s, int) for s in input_tensor_info[node_input].shape)
                and dtype_bytes
            ):
                tensor_size = float(
                    np.prod(np.array(input_tensor_info[node_input].shape))
                )
                input_tensor_info[node_input].size_kbytes = (
                    tensor_size * float(dtype_bytes) / 1024.0
                )

        output_tensor_info = TensorData()
        for node_output in onnx_node.output:
            output_tensor_info[node_output] = TensorInfo()
            if (
                node_output in self.input_tensors_
                or node_output in self.value_tensors_
                or node_output in self.output_tensors_
            ):
                tensor = (
                    self.input_tensors_.get(node_output)
                    or self.value_tensors_.get(node_output)
                    or self.output_tensors_.get(node_output)
                )
                if tensor:
                    output_tensor_info[node_output].shape.extend(
                        [
                            int(dim.dim_value)
                            for dim in tensor.type.tensor_type.shape.dim
                        ]
                    )
                    dtype_str, dtype_bytes = onnx_utils.tensor_type_to_str_and_size(
                        tensor.type.tensor_type.elem_type
                    )
            elif node_output in self.init_tensors_:
                output_tensor_info[node_output].shape.extend(
                    [dim for dim in self.init_tensors_[node_output].dims]
                )
                dtype_str, dtype_bytes = onnx_utils.tensor_type_to_str_and_size(
                    self.init_tensors_[node_output].data_type
                )

            else:
                dtype_str = None
                dtype_bytes = None

            output_tensor_info[node_output].dtype = dtype_str
            output_tensor_info[node_output].dtype_bytes = dtype_bytes

            if (
                all(isinstance(s, int) for s in output_tensor_info[node_output].shape)
                and dtype_bytes
            ):
                tensor_size = float(
                    np.prod(np.array(output_tensor_info[node_output].shape))
                )
                output_tensor_info[node_output].size_kbytes = (
                    tensor_size * float(dtype_bytes) / 1024.0
                )

        return input_tensor_info, output_tensor_info

    def parse_model_nodes(self, onnx_model: onnx.ModelProto) -> None:
        """
        Calculate total number of FLOPs found in the onnx model.
        FLOP is defined as one floating-point operation. This distinguishes
        from multiply-accumulates (MACs) where FLOPs == 2 * MACs.
        """

        # Initialze to zero so we can accumulate. Set to None during the
        # model FLOPs calculation if it errors out.
        self.flops = 0

        # Check to see if the model inputs have any dynamic shapes
        if onnx_utils.get_dynamic_input_dims(onnx_model):
            self.flops = None

        try:
            onnx_model, _ = onnx_utils.optimize_onnx_model(onnx_model)

            onnx_model = onnx.shape_inference.infer_shapes(
                onnx_model, strict_mode=True, data_prop=True
            )
        except Exception as e:  # pylint: disable=broad-except
            print(f"ONNX utils: {str(e)}")
            self.flops = None

        # If the ONNX model contains one of the following unsupported ops, then this
        # function will return None since the FLOP total is expected to be incorrect
        unsupported_ops = [
            "Einsum",
            "RNN",
            "GRU",
            "DeformConv",
        ]

        if not self.input_tensors_:
            self.input_tensors_ = {
                tensor.name: tensor for tensor in onnx_model.graph.input
            }

        if not self.output_tensors_:
            self.output_tensors_ = {
                tensor.name: tensor for tensor in onnx_model.graph.output
            }

        if not self.value_tensors_:
            self.value_tensors_ = {
                tensor.name: tensor for tensor in onnx_model.graph.value_info
            }

        if not self.init_tensors_:
            self.init_tensors_ = {
                tensor.name: tensor for tensor in onnx_model.graph.initializer
            }

        for node in onnx_model.graph.node:  # pylint: disable=E1101

            node_info = NodeInfo()

            # TODO: I have encountered models containing nodes with no name. It would be a good idea
            # to have this type of model info fed back to the user through a warnings section.
            if not node.name:
                node.name = f"{node.op_type}_{len(self.node_data)}"

            node_info.node_type = node.op_type
            input_tensor_info, output_tensor_info = self.get_node_tensor_info_(node)
            node_info.inputs = input_tensor_info
            node_info.outputs = output_tensor_info

            # Check if this node has parameters through the init tensors
            for input_name, input_tensor in node_info.inputs.items():
                if input_name in self.init_tensors_:
                    if all(isinstance(dim, int) for dim in input_tensor.shape):
                        input_parameters = int(np.prod(np.array(input_tensor.shape)))
                        node_info.parameters += input_parameters
                        self.parameters += input_parameters
                        self.node_type_parameters[node.op_type] = (
                            self.node_type_parameters.get(node.op_type, 0)
                            + input_parameters
                        )
                    else:
                        print(f"Tensor with params has unknown shape: {input_name}")

            for attribute in node.attribute:
                node_info.attributes.update(onnx_utils.attribute_to_dict(attribute))

            # if node.name in self.node_data:
            #     print(f"Node name {node.name} is a duplicate.")

            self.node_data[node.name] = node_info

            if node.op_type in unsupported_ops:
                self.flops = None
                node_info.flops = None

            try:

                if (
                    node.op_type == "MatMul"
                    or node.op_type == "MatMulInteger"
                    or node.op_type == "QLinearMatMul"
                ):

                    input_a = node_info.get_input(0).shape
                    if node.op_type == "QLinearMatMul":
                        input_b = node_info.get_input(3).shape
                    else:
                        input_b = node_info.get_input(1).shape

                    if not all(
                        isinstance(dim, int) for dim in input_a
                    ) or not isinstance(input_b[-1], int):
                        node_info.flops = None
                        self.flops = None
                        continue

                    node_info.flops = int(
                        2 * np.prod(np.array(input_a), dtype=np.int64) * input_b[-1]
                    )

                elif (
                    node.op_type == "Mul"
                    or node.op_type == "Div"
                    or node.op_type == "Add"
                ):
                    input_a = node_info.get_input(0).shape
                    input_b = node_info.get_input(1).shape

                    if not all(isinstance(dim, int) for dim in input_a) or not all(
                        isinstance(dim, int) for dim in input_b
                    ):
                        node_info.flops = None
                        self.flops = None
                        continue

                    node_info.flops = int(
                        np.prod(np.array(input_a), dtype=np.int64)
                    ) + int(np.prod(np.array(input_b), dtype=np.int64))

                elif node.op_type == "Gemm" or node.op_type == "QGemm":
                    x_shape = node_info.get_input(0).shape
                    if node.op_type == "Gemm":
                        w_shape = node_info.get_input(1).shape
                    else:
                        w_shape = node_info.get_input(3).shape

                    if not all(isinstance(dim, int) for dim in x_shape) or not all(
                        isinstance(dim, int) for dim in w_shape
                    ):
                        node_info.flops = None
                        self.flops = None
                        continue

                    mm_dims = [
                        (
                            x_shape[0]
                            if not node_info.attributes.get("transA", 0)
                            else x_shape[1]
                        ),
                        (
                            x_shape[1]
                            if not node_info.attributes.get("transA", 0)
                            else x_shape[0]
                        ),
                        (
                            w_shape[1]
                            if not node_info.attributes.get("transB", 0)
                            else w_shape[0]
                        ),
                    ]

                    node_info.flops = int(
                        2 * np.prod(np.array(mm_dims), dtype=np.int64)
                    )

                    if len(mm_dims) == 3:  # if there is a bias input
                        bias_shape = node_info.get_input(2).shape
                        node_info.flops += int(np.prod(np.array(bias_shape)))

                elif (
                    node.op_type == "Conv"
                    or node.op_type == "ConvInteger"
                    or node.op_type == "QLinearConv"
                    or node.op_type == "ConvTranspose"
                ):
                    # N, C, d1, ..., dn
                    x_shape = node_info.get_input(0).shape

                    # M, C/group, k1, ..., kn. Note C and M are swapped for ConvTranspose
                    if node.op_type == "QLinearConv":
                        w_shape = node_info.get_input(3).shape
                    else:
                        w_shape = node_info.get_input(1).shape

                    if not all(isinstance(dim, int) for dim in x_shape):
                        node_info.flops = None
                        self.flops = None
                        continue

                    x_shape_ints = cast(List[int], x_shape)
                    w_shape_ints = cast(List[int], w_shape)

                    has_bias = False  # Note, ConvInteger has no bias
                    if node.op_type == "Conv" and len(node_info.inputs) == 3:
                        has_bias = True
                    elif node.op_type == "QLinearConv" and len(node_info.inputs) == 9:
                        has_bias = True

                    num_dims = len(x_shape_ints) - 2
                    strides = node_info.attributes.get(
                        "strides", [1] * num_dims
                    )  # type: List[int]
                    dilation = node_info.attributes.get(
                        "dilations", [1] * num_dims
                    )  # type: List[int]
                    kernel_shape = w_shape_ints[2:]
                    batch_size = x_shape_ints[0]
                    out_channels = w_shape_ints[0]
                    out_dims = [batch_size, out_channels]
                    output_shape = node_info.attributes.get(
                        "output_shape", []
                    )  # type: List[int]

                    # If output_shape is given then we do not need to compute it ourselves
                    # The output_shape attribute does not include batch_size or channels and
                    # is only valid for ConvTranspose
                    if output_shape:
                        out_dims.extend(output_shape)
                    else:
                        auto_pad = node_info.attributes.get(
                            "auto_pad", "NOTSET".encode()
                        ).decode()
                        # SAME expects padding so that the output_shape = CEIL(input_shape / stride)
                        if auto_pad == "SAME_UPPER" or auto_pad == "SAME_LOWER":
                            out_dims.extend(
                                [x * s for x, s in zip(x_shape_ints[2:], strides)]
                            )
                        else:
                            # NOTSET means just use pads attribute
                            if auto_pad == "NOTSET":
                                pads = node_info.attributes.get(
                                    "pads", [0] * num_dims * 2
                                )
                            # VALID essentially means no padding
                            elif auto_pad == "VALID":
                                pads = [0] * num_dims * 2

                            for i in range(num_dims):
                                dim_in = x_shape_ints[i + 2]  # type: int

                                if node.op_type == "ConvTranspose":
                                    out_dim = (
                                        strides[i] * (dim_in - 1)
                                        + ((kernel_shape[i] - 1) * dilation[i] + 1)
                                        - pads[i]
                                        - pads[i + num_dims]
                                    )
                                else:
                                    out_dim = (
                                        dim_in
                                        + pads[i]
                                        + pads[i + num_dims]
                                        - dilation[i] * (kernel_shape[i] - 1)
                                        - 1
                                    ) // strides[i] + 1

                                out_dims.append(out_dim)

                    kernel_flops = int(
                        np.prod(np.array(kernel_shape)) * w_shape_ints[1]
                    )
                    output_points = int(np.prod(np.array(out_dims)))
                    bias_ops = output_points if has_bias else int(0)
                    node_info.flops = 2 * kernel_flops * output_points + bias_ops

                elif node.op_type == "LSTM" or node.op_type == "DynamicQuantizeLSTM":

                    x_shape = node_info.get_input(
                        0
                    ).shape  # seq_length, batch_size, input_dim

                    if not all(isinstance(dim, int) for dim in x_shape):
                        node_info.flops = None
                        self.flops = None
                        continue

                    x_shape_ints = cast(List[int], x_shape)
                    hidden_size = node_info.attributes["hidden_size"]
                    direction = (
                        2
                        if node_info.attributes.get("direction")
                        == "bidirectional".encode()
                        else 1
                    )

                    has_bias = True if len(node_info.inputs) >= 4 else False
                    if has_bias:
                        bias_shape = node_info.get_input(3).shape
                        if isinstance(bias_shape[1], int):
                            bias_ops = bias_shape[1]
                        else:
                            bias_ops = 0
                    else:
                        bias_ops = 0
                    # seq_length, batch_size, input_dim = x_shape
                    if not isinstance(bias_ops, int):
                        bias_ops = int(0)
                    num_gates = int(4)
                    gate_input_flops = int(2 * x_shape_ints[2] * hidden_size)
                    gate_hid_flops = int(2 * hidden_size * hidden_size)
                    unit_flops = (
                        num_gates * (gate_input_flops + gate_hid_flops) + bias_ops
                    )
                    node_info.flops = (
                        x_shape_ints[1] * x_shape_ints[0] * direction * unit_flops
                    )
                # In this case we just hit an op that doesn't have FLOPs
                else:
                    node_info.flops = None

            except IndexError as err:
                print(f"Error parsing node {node.name}: {err}")
                node_info.flops = None
                self.flops = None
                continue

            # Update the model level flops count
            if node_info.flops is not None and self.flops is not None:
                self.flops += node_info.flops

                # Update the node type flops count
                self.node_type_flops[node.op_type] = (
                    self.node_type_flops.get(node.op_type, 0) + node_info.flops
                )

    def save_yaml_report(self, filepath: str) -> None:

        parent_dir = os.path.dirname(os.path.abspath(filepath))
        if not os.path.exists(parent_dir):
            raise FileNotFoundError(f"Directory {parent_dir} does not exist.")

        report_date = datetime.now().strftime("%B %d, %Y")

        input_tensors = dict({k: vars(v) for k, v in self.model_inputs.items()})
        output_tensors = dict({k: vars(v) for k, v in self.model_outputs.items()})
        digest_version = importlib.metadata.version("digestai")

        yaml_data = {
            "report_date": report_date,
            "digest_version": digest_version,
            "model_type": self.model_type.value,
            "model_file": self.filepath,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "graph_name": self.graph_name,
            "producer_name": self.producer_name,
            "producer_version": self.producer_version,
            "ir_version": self.ir_version,
            "opset": self.opset,
            "import_list": dict(self.imports),
            "graph_nodes": sum(self.node_type_counts.values()),
            "parameters": self.parameters,
            "flops": self.flops,
            "node_type_counts": dict(self.node_type_counts),
            "node_type_flops": dict(self.node_type_flops),
            "node_type_parameters": self.node_type_parameters,
            "input_tensors": input_tensors,
            "output_tensors": output_tensors,
        }

        with open(filepath, "w", encoding="utf-8") as f_p:
            yaml.dump(yaml_data, f_p, sort_keys=False)

    def save_text_report(self, filepath: str) -> None:

        parent_dir = os.path.dirname(os.path.abspath(filepath))
        if not os.path.exists(parent_dir):
            raise FileNotFoundError(f"Directory {parent_dir} does not exist.")

        report_date = datetime.now().strftime("%B %d, %Y")

        digest_version = importlib.metadata.version("digestai")

        with open(filepath, "w", encoding="utf-8") as f_p:
            f_p.write(f"Report created on {report_date}\n")
            f_p.write(f"Digest version: {digest_version}\n")
            f_p.write(f"Model type: {self.model_type.name}\n")
            if self.filepath:
                f_p.write(f"ONNX file: {self.filepath}\n")
            f_p.write(f"Name of the model: {self.model_name}\n")
            f_p.write(f"Model version: {self.model_version}\n")
            f_p.write(f"Name of the graph: {self.graph_name}\n")
            f_p.write(f"Producer: {self.producer_name} {self.producer_version}\n")
            f_p.write(f"Ir version: {self.ir_version}\n")
            f_p.write(f"Opset: {self.opset}\n\n")
            f_p.write("Import list\n")
            for name, version in self.imports.items():
                f_p.write(f"\t{name}: {version}\n")

            f_p.write("\n")
            f_p.write(f"Total graph nodes: {sum(self.node_type_counts.values())}\n")
            f_p.write(f"Number of parameters: {self.parameters}\n")
            if self.flops:
                f_p.write(f"Number of FLOPs: {self.flops}\n")
                f_p.write("\n")

                table_op_intensity = PrettyTable()
                table_op_intensity.field_names = ["Operation", "FLOPs", "Intensity (%)"]
                for op_type, count in self.node_type_flops.items():
                    if count > 0:
                        table_op_intensity.add_row(
                            [
                                op_type,
                                count,
                                100.0 * float(count) / float(self.flops),
                            ]
                        )

                f_p.write("Op intensity:\n")
                f_p.write(table_op_intensity.get_string())
                f_p.write("\n\n")

            node_counts_table = PrettyTable()
            node_counts_table.field_names = ["Node", "Occurrences"]
            for op, count in self.node_type_counts.items():
                node_counts_table.add_row([op, count])
            f_p.write("Nodes and their occurrences:\n")
            f_p.write(node_counts_table.get_string())
            f_p.write("\n\n")

            input_table = PrettyTable()
            input_table.field_names = [
                "Input Name",
                "Shape",
                "Type",
                "Tensor Size (KB)",
            ]
            for input_name, input_details in self.model_inputs.items():
                if input_details.size_kbytes:
                    kbytes = f"{input_details.size_kbytes:.2f}"
                else:
                    kbytes = ""

                input_table.add_row(
                    [
                        input_name,
                        input_details.shape,
                        input_details.dtype,
                        kbytes,
                    ]
                )
            f_p.write("Input Tensor(s) Information:\n")
            f_p.write(input_table.get_string())
            f_p.write("\n\n")

            output_table = PrettyTable()
            output_table.field_names = [
                "Output Name",
                "Shape",
                "Type",
                "Tensor Size (KB)",
            ]
            for output_name, output_details in self.model_outputs.items():
                if output_details.size_kbytes:
                    kbytes = f"{output_details.size_kbytes:.2f}"
                else:
                    kbytes = ""

                output_table.add_row(
                    [
                        output_name,
                        output_details.shape,
                        output_details.dtype,
                        kbytes,
                    ]
                )
            f_p.write("Output Tensor(s) Information:\n")
            f_p.write(output_table.get_string())
            f_p.write("\n\n")
