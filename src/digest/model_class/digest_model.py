# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import csv
from enum import Enum
from dataclasses import dataclass, field
from uuid import uuid4
from abc import ABC, abstractmethod
from collections import Counter, OrderedDict, defaultdict
from typing import List, Dict, Optional, Any, Union


class SupportedModelTypes(Enum):
    ONNX = "onnx"
    REPORT = "report"


class NodeParsingException(Exception):
    pass


# The classes are for type aliasing. Once python 3.10 is the minimum  we can switch to TypeAlias
class NodeShapeCounts(defaultdict[str, Counter]):
    def __init__(self):
        super().__init__(Counter)  # Initialize with the Counter factory


class NodeTypeCounts(Dict[str, int]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class TensorInfo:
    "Used to store node input and output tensor information"
    dtype: Optional[str] = None
    dtype_bytes: Optional[int] = None
    size_kbytes: Optional[float] = None
    shape: List[Union[int, str]] = field(default_factory=list)


class TensorData(OrderedDict[str, TensorInfo]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NodeInfo:
    def __init__(self) -> None:
        self.flops: Optional[int] = None
        self.parameters: int = 0  # TODO: should we make this Optional[int] = None?
        self.node_type: Optional[str] = None
        self.attributes: OrderedDict[str, Any] = OrderedDict()
        # We use an ordered dictionary because the order in which
        # the inputs and outputs are listed in the node matter.
        self.inputs = TensorData()
        self.outputs = TensorData()

    def get_input(self, index: int) -> TensorInfo:
        return list(self.inputs.values())[index]

    def get_output(self, index: int) -> TensorInfo:
        return list(self.outputs.values())[index]

    def __str__(self):
        """Provides a human-readable string representation of NodeInfo."""
        output = [
            f"Node Type: {self.node_type}",
            f"FLOPs: {self.flops if self.flops is not None else 'N/A'}",
            f"Parameters: {self.parameters}",
        ]

        if self.attributes:
            output.append("Attributes:")
            for key, value in self.attributes.items():
                output.append(f"  - {key}: {value}")

        if self.inputs:
            output.append("Inputs:")
            for name, tensor in self.inputs.items():
                output.append(f"  - {name}: {tensor}")

        if self.outputs:
            output.append("Outputs:")
            for name, tensor in self.outputs.items():
                output.append(f"  - {name}: {tensor}")

        return "\n".join(output)


# The classes are for type aliasing. Once python 3.10 is the minimum we can switch to TypeAlias
class NodeData(OrderedDict[str, NodeInfo]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DigestModel(ABC):
    def __init__(self, filepath: str, model_name: str):
        # Public members exposed to the API
        self.unique_id: str = str(uuid4())
        self.filepath: Optional[str] = filepath
        self.model_name: str = model_name
        self.model_type: Optional[SupportedModelTypes] = None
        self.node_type_counts: NodeTypeCounts = NodeTypeCounts()
        self.model_flops: Optional[int] = None
        self.model_parameters: int = 0
        self.node_type_flops: Dict[str, int] = {}
        self.node_type_parameters: Dict[str, int] = {}
        self.node_data = NodeData()
        self.model_inputs = TensorData()
        self.model_outputs = TensorData()

    def get_node_shape_counts(self) -> NodeShapeCounts:
        tensor_shape_counter = NodeShapeCounts()
        for _, info in self.node_data.items():
            shape_hash = tuple([tuple(v.shape) for _, v in info.inputs.items()])
            if info.node_type:
                tensor_shape_counter[info.node_type][shape_hash] += 1
        return tensor_shape_counter

    @abstractmethod
    def parse_model_nodes(self, *args) -> None:
        pass

    @abstractmethod
    def save_yaml_report(self, filepath: str) -> None:
        pass

    @abstractmethod
    def save_text_report(self, filepath: str) -> None:
        pass

    def save_nodes_csv_report(self, filepath: str) -> None:
        save_nodes_csv_report(self.node_data, filepath)

    def save_node_type_counts_csv_report(self, filepath: str) -> None:
        if self.node_type_counts:
            save_node_type_counts_csv_report(self.node_type_counts, filepath)

    def save_node_shape_counts_csv_report(self, filepath: str) -> None:
        save_node_shape_counts_csv_report(self.get_node_shape_counts(), filepath)


def save_nodes_csv_report(node_data: NodeData, filepath: str) -> None:

    parent_dir = os.path.dirname(os.path.abspath(filepath))
    if not os.path.exists(parent_dir):
        raise FileNotFoundError(f"Directory {parent_dir} does not exist.")

    flattened_data = []
    fieldnames = ["Node Name", "Node Type", "Parameters", "FLOPs", "Attributes"]
    input_fieldnames = []
    output_fieldnames = []
    for name, node_info in node_data.items():
        row = OrderedDict()
        row["Node Name"] = name
        row["Node Type"] = str(node_info.node_type)
        row["Parameters"] = str(node_info.parameters)
        row["FLOPs"] = str(node_info.flops)
        if node_info.attributes:
            row["Attributes"] = str({k: v for k, v in node_info.attributes.items()})
        else:
            row["Attributes"] = ""

        for i, (input_name, input_info) in enumerate(node_info.inputs.items()):
            column_name = f"Input{i+1} (Shape, Dtype, Size (kB))"
            row[column_name] = (
                f"{input_name} ({input_info.shape}, {input_info.dtype}, {input_info.size_kbytes})"
            )

            # Dynamically add input column names to fieldnames if not already present
            if column_name not in input_fieldnames:
                input_fieldnames.append(column_name)

        for i, (output_name, output_info) in enumerate(node_info.outputs.items()):
            column_name = f"Output{i+1} (Shape, Dtype, Size (kB))"
            row[column_name] = (
                f"{output_name} ({output_info.shape}, "
                f"{output_info.dtype}, {output_info.size_kbytes})"
            )

            # Dynamically add input column names to fieldnames if not already present
            if column_name not in output_fieldnames:
                output_fieldnames.append(column_name)

        flattened_data.append(row)

    fieldnames = fieldnames + input_fieldnames + output_fieldnames
    with open(filepath, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(flattened_data)


def save_node_type_counts_csv_report(
    node_type_counts: NodeTypeCounts, filepath: str
) -> None:

    parent_dir = os.path.dirname(os.path.abspath(filepath))
    if not os.path.exists(parent_dir):
        raise FileNotFoundError(f"Directory {parent_dir} does not exist.")

    header = ["Node Type", "Count"]

    with open(filepath, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, lineterminator="\n")
        writer.writerow(header)
        for node_type, node_count in node_type_counts.items():
            writer.writerow([node_type, node_count])


def save_node_shape_counts_csv_report(
    node_shape_counts: NodeShapeCounts, filepath: str
) -> None:

    parent_dir = os.path.dirname(os.path.abspath(filepath))
    if not os.path.exists(parent_dir):
        raise FileNotFoundError(f"Directory {parent_dir} does not exist.")

    header = ["Node Type", "Input Tensors Shapes", "Count"]

    with open(filepath, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, dialect="excel", lineterminator="\n")
        writer.writerow(header)
        for node_type, node_info in node_shape_counts.items():
            info_iter = iter(node_info.items())
            for shape, count in info_iter:
                writer.writerow([node_type, shape, count])
