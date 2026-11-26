# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import hashlib
import zipfile
from pathlib import Path
import pandas as pd
from platformdirs import user_cache_path

from digest.subgraph_analysis.model_encode import (
    encode_model,
)


def _target_cache_path(model_path, dequantize=False, cache_dir=None):
    model_hash = hashlib.sha256()
    model_hash.update(b"dequantize=true\0" if dequantize else b"dequantize=false\0")
    with open(model_path, "rb") as model_file:
        for chunk in iter(lambda: model_file.read(1024 * 1024), b""):
            model_hash.update(chunk)

    cache_root = Path(cache_dir) if cache_dir else user_cache_path("digestai")
    return cache_root / "similarity" / "targets" / f"{model_hash.hexdigest()}.json"


def find_match(
    model_path,
    dequantize=False,
    replace=False,
    cache_dir=None,
    database_zip_path=None,
):
    target_model_path = _target_cache_path(model_path, dequantize, cache_dir)
    if replace or not target_model_path.exists():
        encode_model(
            model_path=model_path,
            dequantize=dequantize,
            output_path=target_model_path,
        )

    with open(target_model_path, "r", encoding="utf-8") as json_file:
        target_model = json.load(json_file)

    # Filter columns we will show
    target_op_dict = dict(target_model["op_list"])
    target_op_dict.pop("input", None)
    target_op_dict.pop("output", None)

    # Only keep the top num_subgraphs subgraphs and all ops
    num_subgraphs = 20
    subgraphs = {k: v for k, v in target_op_dict.items() if len(k) == 32}
    subgraphs = sorted(subgraphs, key=subgraphs.get, reverse=True)[:num_subgraphs]
    ops = list({k: v for k, v in target_op_dict.items() if len(k) != 32}.keys())
    target_op_dict = {k: v for k, v in target_op_dict.items() if k in subgraphs + ops}
    if not target_op_dict:
        raise ValueError("The target model does not contain comparable operations.")

    database_zip_path = database_zip_path or Path(__file__).with_name("database.zip")
    rows = []
    with zipfile.ZipFile(database_zip_path, "r") as database_zip:
        reference_files = sorted(
            name for name in database_zip.namelist() if name.endswith(".json")
        )
        for reference_json in reference_files:
            reference_name = Path(reference_json).stem
            reference_model = json.loads(database_zip.read(reference_json))

            score = 0
            row = {"Name": reference_name}

            for subgraph in target_op_dict:
                if subgraph in reference_model["op_list"]:

                    ratio = (
                        reference_model["op_list"][subgraph]
                        / target_op_dict[subgraph]
                    )
                    if ratio > 1:
                        ratio = 1 / ratio
                    row[subgraph] = ratio
                    score += row[subgraph]
                else:
                    row[subgraph] = 0.0
            row["Score"] = score / len(target_op_dict)
            rows.append(row)

    if not rows:
        raise ValueError("The similarity reference database is empty.")

    df = pd.DataFrame(rows, columns=["Name", "Score"] + list(target_op_dict))

    # Convert to pandas and sort by score
    df_sorted = df.sort_values(by="Score", ascending=False)

    # Only keep top and bottom values
    if len(df_sorted) > 30:
        df_sorted = pd.concat([df_sorted.head(25), df_sorted.tail(5)])

    name_list = df_sorted["Name"].tolist()
    df_sorted = df_sorted.drop(columns=["Score", "Name"]).reset_index(drop=True)

    return name_list, target_model, df_sorted


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
