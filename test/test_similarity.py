# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

import json
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest

from digest.subgraph_analysis.find_match import _target_cache_path, find_match


def _write_database(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as database:
        database.writestr("database/close.json", json.dumps({"op_list": {"Conv": 4}}))
        database.writestr("database/far.json", json.dumps({"op_list": {"Conv": 1}}))


def _encode_target(*, output_path, **_kwargs) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"op_list": {"Conv": 4}}), encoding="utf-8")


def test_target_cache_uses_content_hash_not_basename(tmp_path):
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first = first_dir / "model.onnx"
    second = second_dir / "model.onnx"
    first.write_bytes(b"first model")
    second.write_bytes(b"second model")

    assert _target_cache_path(first, cache_dir=tmp_path) != _target_cache_path(
        second, cache_dir=tmp_path
    )


def test_similarity_reads_immutable_zip_and_writes_user_cache(tmp_path):
    model = tmp_path / "model.onnx"
    model.write_bytes(b"model")
    database = tmp_path / "database.zip"
    _write_database(database)

    with patch(
        "digest.subgraph_analysis.find_match.encode_model",
        side_effect=_encode_target,
    ):
        names, _, scores = find_match(
            model,
            cache_dir=tmp_path / "cache",
            database_zip_path=database,
        )

    assert names == ["close", "far"]
    assert scores.shape == (2, 1)
    assert len(list((tmp_path / "cache").rglob("*.json"))) == 1


def test_empty_target_operations_are_rejected(tmp_path):
    model = tmp_path / "model.onnx"
    model.write_bytes(b"model")
    database = tmp_path / "database.zip"
    _write_database(database)

    def encode_empty(*, output_path, **_kwargs):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps({"op_list": {}}), encoding="utf-8")

    with patch(
        "digest.subgraph_analysis.find_match.encode_model",
        side_effect=encode_empty,
    ), pytest.raises(ValueError, match="comparable operations"):
        find_match(
            model,
            cache_dir=tmp_path / "cache",
            database_zip_path=database,
        )
