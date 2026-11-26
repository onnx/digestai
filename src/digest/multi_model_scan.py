# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml


REPORT_KEYS = {
    "report_date",
    "model_file",
    "model_type",
    "model_name",
    "flops",
    "node_type_flops",
    "node_type_parameters",
    "node_type_counts",
    "input_tensors",
    "output_tensors",
}
VOLATILE_REPORT_KEYS = {"report_date", "model_file", "digest_version"}


@dataclass
class ScanResult:
    onnx_groups: list[list[str]]
    report_groups: list[list[str]]
    errors: list[str]
    total_files: int
    canceled: bool = False


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _report_digest(path: Path) -> str:
    with path.open("r", encoding="utf-8") as file:
        report = yaml.safe_load(file)
    if not isinstance(report, dict) or not REPORT_KEYS <= report.keys():
        raise ValueError("not a Digest report")
    normalized = {
        key: value for key, value in report.items() if key not in VOLATILE_REPORT_KEYS
    }
    serialized = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def scan_directory(
    directory: str,
    *,
    canceled: Callable[[], bool] = lambda: False,
    progress: Callable[[], None] = lambda: None,
) -> ScanResult:
    root = Path(directory)
    onnx_files = sorted(root.rglob("*.onnx"))
    report_files = sorted(root.rglob("*.yaml"))
    total_files = len(onnx_files) + len(report_files)

    onnx_groups: defaultdict[str, list[str]] = defaultdict(list)
    report_groups: defaultdict[str, list[str]] = defaultdict(list)
    errors = []

    for path in onnx_files:
        if canceled():
            return ScanResult([], [], errors, total_files, canceled=True)
        try:
            onnx_groups[_file_digest(path)].append(str(path))
        except OSError as error:
            errors.append(f"{path}: {error}")
        progress()

    for path in report_files:
        if canceled():
            return ScanResult([], [], errors, total_files, canceled=True)
        try:
            report_groups[_report_digest(path)].append(str(path))
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            errors.append(f"{path}: {error}")
        progress()

    return ScanResult(
        list(onnx_groups.values()),
        list(report_groups.values()),
        errors,
        total_files,
    )
