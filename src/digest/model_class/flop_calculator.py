# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from typing import List, Optional, cast

import numpy as np
import onnx

from digest.model_class.digest_model import NodeInfo


@dataclass(frozen=True)
class FlopCalculation:
    flops: Optional[int]
    complete: bool = True


def calculate_node_flops(
    node: onnx.NodeProto, node_info: NodeInfo
) -> FlopCalculation:
    """Calculate one node's FLOPs without mutating model-level state."""
    try:
        if node.op_type in {"MatMul", "MatMulInteger", "QLinearMatMul"}:
            input_a = node_info.get_input(0).shape
            output_shape = node_info.get_output(0).shape
            if (
                not all(isinstance(dim, int) for dim in output_shape)
                or not input_a
                or not isinstance(input_a[-1], int)
            ):
                return FlopCalculation(None, complete=False)
            return FlopCalculation(
                int(
                    2
                    * np.prod(np.array(output_shape), dtype=np.int64)
                    * input_a[-1]
                )
            )

        if node.op_type in {"Mul", "Div", "Add"}:
            output_shape = node_info.get_output(0).shape
            if not all(isinstance(dim, int) for dim in output_shape):
                return FlopCalculation(None, complete=False)
            return FlopCalculation(
                int(np.prod(np.array(output_shape), dtype=np.int64))
            )

        if node.op_type in {"Gemm", "QGemm"}:
            x_shape = node_info.get_input(0).shape
            weight_index = 1 if node.op_type == "Gemm" else 3
            w_shape = node_info.get_input(weight_index).shape
            if not all(isinstance(dim, int) for dim in x_shape) or not all(
                isinstance(dim, int) for dim in w_shape
            ):
                return FlopCalculation(None, complete=False)

            mm_dims = [
                x_shape[0]
                if not node_info.attributes.get("transA", 0)
                else x_shape[1],
                x_shape[1]
                if not node_info.attributes.get("transA", 0)
                else x_shape[0],
                w_shape[1]
                if not node_info.attributes.get("transB", 0)
                else w_shape[0],
            ]
            flops = int(2 * np.prod(np.array(mm_dims), dtype=np.int64))
            bias_index = 2 if node.op_type == "Gemm" else 6
            if len(node.input) > bias_index and node.input[bias_index]:
                flops += mm_dims[0] * mm_dims[2]
            return FlopCalculation(flops)

        if node.op_type in {
            "Conv",
            "ConvInteger",
            "QLinearConv",
            "ConvTranspose",
        }:
            x_shape = node_info.get_input(0).shape
            weight_index = 3 if node.op_type == "QLinearConv" else 1
            w_shape = node_info.get_input(weight_index).shape
            if not all(isinstance(dim, int) for dim in x_shape) or not all(
                isinstance(dim, int) for dim in w_shape
            ):
                return FlopCalculation(None, complete=False)

            x_shape_ints = cast(List[int], x_shape)
            w_shape_ints = cast(List[int], w_shape)
            has_bias = (
                node.op_type in {"Conv", "ConvTranspose"}
                and len(node_info.inputs) == 3
            ) or (node.op_type == "QLinearConv" and len(node_info.inputs) == 9)

            num_dims = len(x_shape_ints) - 2
            strides: List[int] = node_info.attributes.get("strides", [1] * num_dims)
            dilation: List[int] = node_info.attributes.get(
                "dilations", [1] * num_dims
            )
            kernel_shape = w_shape_ints[2:]
            group = node_info.attributes.get("group", 1)
            out_channels = (
                w_shape_ints[1] * group
                if node.op_type == "ConvTranspose"
                else w_shape_ints[0]
            )
            out_dims = [x_shape_ints[0], out_channels]
            output_shape: List[int] = node_info.attributes.get("output_shape", [])

            if output_shape:
                out_dims.extend(output_shape)
            else:
                auto_pad = node_info.attributes.get(
                    "auto_pad", "NOTSET".encode()
                ).decode()
                if auto_pad in {"SAME_UPPER", "SAME_LOWER"}:
                    out_dims.extend(
                        (dimension + stride - 1) // stride
                        for dimension, stride in zip(x_shape_ints[2:], strides)
                    )
                else:
                    pads = (
                        node_info.attributes.get("pads", [0] * num_dims * 2)
                        if auto_pad == "NOTSET"
                        else [0] * num_dims * 2
                    )
                    output_padding = node_info.attributes.get(
                        "output_padding", [0] * num_dims
                    )
                    for index in range(num_dims):
                        dim_in = x_shape_ints[index + 2]
                        if node.op_type == "ConvTranspose":
                            out_dim = (
                                strides[index] * (dim_in - 1)
                                + ((kernel_shape[index] - 1) * dilation[index] + 1)
                                - pads[index]
                                - pads[index + num_dims]
                                + output_padding[index]
                            )
                        else:
                            out_dim = (
                                dim_in
                                + pads[index]
                                + pads[index + num_dims]
                                - dilation[index] * (kernel_shape[index] - 1)
                                - 1
                            ) // strides[index] + 1
                        out_dims.append(out_dim)

            channels_per_output = (
                w_shape_ints[0] // group
                if node.op_type == "ConvTranspose"
                else w_shape_ints[1]
            )
            kernel_flops = int(np.prod(np.array(kernel_shape)) * channels_per_output)
            output_points = int(np.prod(np.array(out_dims)))
            bias_ops = output_points if has_bias else 0
            return FlopCalculation(2 * kernel_flops * output_points + bias_ops)

        if node.op_type in {"LSTM", "DynamicQuantizeLSTM"}:
            x_shape = node_info.get_input(0).shape
            if not all(isinstance(dim, int) for dim in x_shape):
                return FlopCalculation(None, complete=False)

            x_shape_ints = cast(List[int], x_shape)
            hidden_size = node_info.attributes["hidden_size"]
            direction = (
                2
                if node_info.attributes.get("direction") == "bidirectional".encode()
                else 1
            )
            bias_ops = 0
            if len(node_info.inputs) >= 4:
                bias_shape = node_info.get_input(3).shape
                if len(bias_shape) > 1 and isinstance(bias_shape[1], int):
                    bias_ops = bias_shape[1]
            gate_input_flops = 2 * x_shape_ints[2] * hidden_size
            gate_hidden_flops = 2 * hidden_size * hidden_size
            unit_flops = 4 * (gate_input_flops + gate_hidden_flops) + bias_ops
            return FlopCalculation(
                x_shape_ints[1] * x_shape_ints[0] * direction * unit_flops
            )

        return FlopCalculation(None)
    except (IndexError, KeyError, TypeError, ZeroDivisionError):
        return FlopCalculation(None, complete=False)
