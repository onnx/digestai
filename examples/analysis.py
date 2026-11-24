# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import argparse
import glob
import csv
from collections import Counter, defaultdict
from tqdm import tqdm
from digest.model_class.digest_model import (
    NodeShapeCounts,
    NodeTypeCounts,
    save_node_shape_counts_csv_report,
    save_node_type_counts_csv_report,
)
from digest.model_class.digest_onnx_model import DigestOnnxModel
from utils.onnx_utils import (
    get_dynamic_input_dims,
    load_onnx,
)

GLOBAL_MODEL_HEADERS = [
    "Model",
    "Opset",
    "Parameters",
    "FLOPs",
]


def main(onnx_files: str, output_dir: str):

    # Check if the provided input is a filepath or directory
    if os.path.isfile(onnx_files) and os.path.splitext(onnx_files)[1] == ".onnx":
        onnx_file_list = [onnx_files]
    elif os.path.isdir(onnx_files):
        onnx_file_list = list(
            glob.glob(os.path.join(onnx_files, "**/*.onnx"), recursive=True)
        )
    else:
        raise FileExistsError(
            "The input must either be an ONNX file or a directory containing "
            f"one or more ONNX files. Got {onnx_files}"
        )

    # Check if the provided output path exists since we won't create it
    if not os.path.exists(output_dir):
        raise FileExistsError(
            f"The directory {os.path.abspath(output_dir)} does not exist; please create it."
        )

    print(f"Processing {len(onnx_file_list)} onnx models.")

    # Holds the data for node type counts across all models
    global_node_type_counter: Counter[str] = Counter()

    # Holds the data for node shape counts across all models
    global_node_shape_counter: NodeShapeCounts = defaultdict(Counter)

    # Holds the data for all models statistics
    global_model_data = {}

    for onnx_file in (pbar := tqdm(onnx_file_list)):
        pbar.set_description(f"Analyzing model {onnx_file}")
        model_name = os.path.splitext(os.path.basename(onnx_file))[0]
        model_proto = load_onnx(onnx_file, False)

        dynamic_input_dims = get_dynamic_input_dims(model_proto)
        if dynamic_input_dims:
            print(
                "Found the following non-static input dims in your model. "
                "It is recommended to make all dims static before generating reports."
            )
            for dynamic_shape in dynamic_input_dims:
                print(f"dim: {dynamic_shape}")

        digest_model = DigestOnnxModel(
            model_proto, onnx_filepath=onnx_file, model_name=model_name
        )

        # Update the global model dictionary
        if model_name in global_model_data:
            print(
                f"Warning! {model_name} has already been processed, skipping the duplicate model."
            )

        global_model_data[model_name] = {
            "opset": digest_model.opset,
            "parameters": digest_model.parameters,
            "flops": digest_model.flops,
        }

        # Model summary text report
        summary_filepath = os.path.join(output_dir, f"{model_name}_summary.txt")
        digest_model.save_text_report(summary_filepath)

        # Model summary yaml report
        summary_filepath = os.path.join(output_dir, f"{model_name}_summary.yaml")
        digest_model.save_yaml_report(summary_filepath)

        # Save csv containing node-level information
        nodes_filepath = os.path.join(output_dir, f"{model_name}_nodes.csv")
        digest_model.save_nodes_csv_report(nodes_filepath)

        # Save csv containing node type counter
        node_type_filepath = os.path.join(
            output_dir, f"{model_name}_node_type_counts.csv"
        )

        digest_model.save_node_type_counts_csv_report(node_type_filepath)

        # Update global data structure for node type counter
        global_node_type_counter.update(digest_model.node_type_counts)

        # Save csv containing node shape counts per op_type
        node_shape_filepath = os.path.join(
            output_dir, f"{model_name}_node_shape_counts.csv"
        )
        digest_model.save_node_shape_counts_csv_report(node_shape_filepath)

        # Update global data structure for node shape counter
        for node_type, shape_counts in digest_model.get_node_shape_counts().items():
            global_node_shape_counter[node_type].update(shape_counts)

    if len(onnx_file_list) > 1:
        global_filepath = os.path.join(output_dir, "global_node_type_counts.csv")
        global_node_type_counts = NodeTypeCounts(global_node_type_counter.most_common())
        save_node_type_counts_csv_report(global_node_type_counts, global_filepath)

        global_filepath = os.path.join(output_dir, "global_node_shape_counts.csv")
        save_node_shape_counts_csv_report(global_node_shape_counter, global_filepath)

        global_filepath = os.path.join(output_dir, "global_model_summary.csv")
        with open(global_filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            rows = [
                [model, data["opset"], data["parameters"], data["flops"]]
                for model, data in global_model_data.items()
            ]
            writer.writerow(GLOBAL_MODEL_HEADERS)
            writer.writerows(rows)

    print(f"Saved all reports to {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate model analysis reports for one or more ONNX models."
    )
    parser.add_argument(
        "onnx_files", type=str, help="Filepath or directory to onnx file(s)."
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="Directory to save text report and csv files.",
    )

    args = parser.parse_args()

    main(args.onnx_files, args.output_dir)
