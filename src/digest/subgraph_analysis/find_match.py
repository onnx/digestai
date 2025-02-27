# Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.

import os
import argparse
import json
import zipfile
import pandas as pd

import numpy as np
from digest.subgraph_analysis.model_encode import (
    encode_model,
)  # pylint: disable=import-error


def find_match(model_path, dequantize=False, replace=False):

    # Unzip database if needed
    analyzer_path = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(analyzer_path, "database")
    if not os.path.exists(database_path):
        database_zip_path = os.path.join(analyzer_path, "database.zip")
        with zipfile.ZipFile(database_zip_path, "r") as zip_ref:
            print("Unpacking model database")
            zip_ref.extractall(analyzer_path)

    # Open feature of target model
    model_name = os.path.splitext(os.path.basename(model_path))[0]
    target_model_path = os.path.join(database_path, f"{model_name}.json")
    if os.path.exists(target_model_path):
        print(f"{target_model_path} found.")
        if replace:
            print("Replacing it!")
            encode_model(model_path=model_path, dequantize=dequantize)
        else:
            print(
                "Using encoded model found in the cache. Use `--replace` "
                "if you want to overwrite it."
            )
    else:
        print("Encoding model for the first time.")
        encode_model(model_path=model_path, dequantize=dequantize)

    with open(target_model_path, "r", encoding="utf-8") as json_file:
        target_model = json.load(json_file)

    # Get features of all models in the database
    # Note that the target model is intentionally part of this list
    models_json = []
    for root, _, files in os.walk(database_path):
        for file in files:
            if file.endswith(".json"):
                models_json.append(os.path.join(root, file))

    # Filter columns we will show
    target_op_dict = target_model["op_list"]
    target_op_dict.pop("input", None)
    target_op_dict.pop("output", None)

    # Only keep the top num_subgraphs subgraphs and all ops
    num_subgraphs = 20
    subgraphs = {k: v for k, v in target_op_dict.items() if len(k) == 32}
    subgraphs = sorted(subgraphs, key=subgraphs.get, reverse=True)[:num_subgraphs]
    ops = list({k: v for k, v in target_op_dict.items() if len(k) != 32}.keys())
    target_op_dict = {k: v for k, v in target_op_dict.items() if k in subgraphs + ops}

    df = pd.DataFrame(columns=["Name", "Score"] + list(target_op_dict))

    scores = {}
    for reference_json in models_json:
        reference_basename = os.path.basename(reference_json)
        reference_name = os.path.splitext(reference_basename)[0]
        with open(reference_json, "r", encoding="utf-8") as ref_json_f:
            reference_model = json.load(ref_json_f)

        score = 0
        row = {"Name": reference_name}

        for subgraph in target_op_dict:
            if subgraph in reference_model["op_list"]:

                ratio = reference_model["op_list"][subgraph] / target_op_dict[subgraph]
                if ratio > 1:
                    ratio = 1 / ratio
                row[subgraph] = ratio
                score += row[subgraph]
            else:
                row[subgraph] = 0.0
        score = score / len(target_op_dict)
        row["Score"] = score
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        scores[reference_name] = score

    # Convert to pandas and sort by score
    df_sorted = df.sort_values(by="Score", ascending=False)

    # Only keep top and bottom values
    df_sorted = pd.concat([df_sorted.head(25), df_sorted.tail(5)])

    name_list = df_sorted["Name"].tolist()
    df_sorted.drop("Score", axis=1, inplace=True)
    df_sorted.drop("Name", axis=1, inplace=True)
    df_sorted = pd.DataFrame(
        np.array(df_sorted.values),
        index=range(len(name_list)),
        columns=df_sorted.columns,
    )

    return name_list, reference_model, df_sorted


def main():
    parser = argparse.ArgumentParser(description="Subgraph Similarity Plot")
    parser.add_argument("model_path", type=str, help="Path to the ONNX model file")
    parser.add_argument(
        "--dequantize", action="store_true", help="Remove quantization nodes"
    )
    parser.add_argument(
        "--replace", action="store_true", help="Replace models previously encoded"
    )

    args = parser.parse_args()
    find_match(args.model_path, args.dequantize, args.replace)


if __name__ == "__main__":
    main()
