import os
from collections import OrderedDict
import csv
import ast
import re
from typing import Tuple, Optional
import yaml
from digest.model_class.digest_model import (
    DigestModel,
    SupportedModelTypes,
    NodeData,
    NodeInfo,
    TensorData,
    TensorInfo,
)


def parse_tensor_info(csv_tensor_cell_value) -> Tuple[str, list, str, float]:
    """This is a helper function that expects the input to come from parsing
    the nodes csv and extracting either an input or output tensor."""

    # Use regex to split the string into name and details
    match = re.match(r"(.*?)\s*\((.*)\)$", csv_tensor_cell_value)
    if not match:
        raise ValueError(f"Invalid format for tensor info: {csv_tensor_cell_value}")

    name, details = match.groups()

    # Split details, but keep the shape as a single item
    match = re.match(r"(\[.*?\])\s*,\s*(.*?)\s*,\s*(.*)", details)
    if not match:
        raise ValueError(f"Invalid format for tensor details: {details}")

    shape_str, dtype, size = match.groups()

    # Ensure shape is stored as a list
    shape = ast.literal_eval(shape_str)
    if not isinstance(shape, list):
        shape = list(shape)

    return name.strip(), shape, dtype.strip(), float(size.split()[0])


class DigestReportModel(DigestModel):
    def __init__(
        self,
        report_filepath: str,
    ) -> None:

        self.model_type = SupportedModelTypes.REPORT

        self.model_data = OrderedDict()
        with open(report_filepath, "r", encoding="utf-8") as yaml_f:
            self.model_data = yaml.safe_load(yaml_f)

        model_name = self.model_data["model_name"]
        super().__init__(report_filepath, model_name)

        self.similarity_heatmap_path: Optional[str] = None
        self.node_data = NodeData()

        # Given the path to the digest report, let's check if its a complete cache
        # and we can grab the nodes csv data and the similarity heatmap
        cache_dir = os.path.dirname(os.path.abspath(report_filepath))
        expected_heatmap_file = os.path.join(cache_dir, f"{model_name}_heatmap.png")
        if os.path.exists(expected_heatmap_file):
            self.similarity_heatmap_path = expected_heatmap_file

        expected_nodes_file = os.path.join(cache_dir, f"{model_name}_nodes.csv")
        if os.path.exists(expected_nodes_file):
            with open(expected_nodes_file, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    node_name = row["Node Name"]
                    node_info = NodeInfo()
                    node_info.node_type = row["Node Type"]
                    if row["Parameters"]:
                        node_info.parameters = int(row["Parameters"])
                    if ast.literal_eval(row["FLOPs"]):
                        node_info.flops = int(row["FLOPs"])
                    node_info.attributes = (
                        OrderedDict(ast.literal_eval(row["Attributes"]))
                        if row["Attributes"]
                        else OrderedDict()
                    )

                    node_info.inputs = TensorData()
                    node_info.outputs = TensorData()

                    # Process inputs and outputs
                    for key, value in row.items():
                        if key.startswith("Input") and value:
                            input_name, shape, dtype, size = parse_tensor_info(value)
                            node_info.inputs[input_name] = TensorInfo()
                            node_info.inputs[input_name].shape = shape
                            node_info.inputs[input_name].dtype = dtype
                            node_info.inputs[input_name].size_kbytes = size

                        elif key.startswith("Output") and value:
                            output_name, shape, dtype, size = parse_tensor_info(value)
                            node_info.outputs[output_name] = TensorInfo()
                            node_info.outputs[output_name].shape = shape
                            node_info.outputs[output_name].dtype = dtype
                            node_info.outputs[output_name].size_kbytes = size

                    self.node_data[node_name] = node_info

        # Unpack the model type agnostic values
        self.model_flops = self.model_data["model_flops"]
        self.model_parameters = self.model_data["model_parameters"]
        self.node_type_flops = self.model_data["node_type_flops"]
        self.node_type_parameters = self.model_data["node_type_parameters"]
        self.node_type_counts = self.model_data["node_type_counts"]

        self.model_inputs = TensorData(
            {
                key: TensorInfo(**val)
                for key, val in self.model_data["input_tensors"].items()
            }
        )
        self.model_outputs = TensorData(
            {
                key: TensorInfo(**val)
                for key, val in self.model_data["output_tensors"].items()
            }
        )

    def parse_model_nodes(self) -> None:
        """There are no model nodes to parse"""

    def save_yaml_report(self, filepath: str) -> None:
        """Report models are not intended to be saved"""

    def save_text_report(self, filepath: str) -> None:
        """Report models are not intended to be saved"""