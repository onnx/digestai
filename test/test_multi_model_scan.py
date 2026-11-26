# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

import yaml

from digest.multi_model_scan import scan_directory


def _report(model_name: str, report_date: str) -> dict:
    return {
        "report_date": report_date,
        "digest_version": "1.2.0",
        "model_file": f"{model_name}.onnx",
        "model_type": "onnx",
        "model_name": model_name,
        "flops": 1,
        "node_type_flops": {},
        "node_type_parameters": {},
        "node_type_counts": {},
        "input_tensors": {},
        "output_tensors": {},
    }


def test_scan_groups_models_without_loading_them(tmp_path):
    (tmp_path / "first.onnx").write_bytes(b"same model")
    (tmp_path / "second.onnx").write_bytes(b"same model")
    (tmp_path / "unique.onnx").write_bytes(b"unique model")

    result = scan_directory(str(tmp_path))

    assert sorted(len(group) for group in result.onnx_groups) == [1, 2]
    assert result.total_files == 3
    assert result.errors == []


def test_report_grouping_ignores_volatile_metadata(tmp_path):
    first = _report("model", "January 1, 2026")
    second = _report("model", "January 2, 2026")
    second["digest_version"] = "1.3.0"
    second["model_file"] = "elsewhere/model.onnx"
    (tmp_path / "first.yaml").write_text(yaml.safe_dump(first), encoding="utf-8")
    (tmp_path / "second.yaml").write_text(yaml.safe_dump(second), encoding="utf-8")
    (tmp_path / "invalid.yaml").write_text("not: a report", encoding="utf-8")

    result = scan_directory(str(tmp_path))

    assert [len(group) for group in result.report_groups] == [2]
    assert len(result.errors) == 1


def test_scan_can_be_canceled_before_reading_files(tmp_path):
    (tmp_path / "model.onnx").write_bytes(b"model")

    result = scan_directory(str(tmp_path), canceled=lambda: True)

    assert result.canceled
    assert result.onnx_groups == []
