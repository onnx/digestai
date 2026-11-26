# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any


REPORT_SCHEMA_VERSION = 1

REQUIRED_FIELD_TYPES = {
    "report_date": (str,),
    "model_file": (str, type(None)),
    "model_type": (str,),
    "model_name": (str,),
    "parameters": (int,),
    "flops": (int, type(None)),
    "node_type_flops": (dict,),
    "node_type_parameters": (dict,),
    "node_type_counts": (dict,),
    "input_tensors": (dict,),
    "output_tensors": (dict,),
}


def validate_report_data(report: Any) -> list[str]:
    if not isinstance(report, dict):
        return ["report must be a mapping"]

    errors = []
    version = report.get("report_schema_version", REPORT_SCHEMA_VERSION)
    if not isinstance(version, int):
        errors.append("report_schema_version must be an integer")
    elif version != REPORT_SCHEMA_VERSION:
        errors.append(
            f"unsupported report_schema_version {version}; "
            f"expected {REPORT_SCHEMA_VERSION}"
        )

    for field, expected_types in REQUIRED_FIELD_TYPES.items():
        if field not in report:
            errors.append(f"missing required field {field}")
        elif not isinstance(report[field], expected_types):
            expected = " or ".join(type_.__name__ for type_ in expected_types)
            errors.append(f"{field} must be {expected}")

    for field in ("node_type_flops", "node_type_parameters", "node_type_counts"):
        values = report.get(field)
        if isinstance(values, dict) and not all(
            isinstance(key, str) and isinstance(value, int)
            for key, value in values.items()
        ):
            errors.append(f"{field} must map strings to integers")

    for field in ("input_tensors", "output_tensors"):
        tensors = report.get(field)
        if not isinstance(tensors, dict):
            continue
        for tensor_name, tensor in tensors.items():
            if not isinstance(tensor_name, str) or not isinstance(tensor, dict):
                errors.append(f"{field} must map tensor names to mappings")
                break
            if not isinstance(tensor.get("shape"), list):
                errors.append(f"{field}.{tensor_name}.shape must be a list")

    return errors
