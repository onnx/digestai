# Copyright (c) ONNX Project Contributors
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from unittest.mock import MagicMock, patch

import onnx
import pytest
import yaml
from PySide6.QtWidgets import QApplication, QFormLayout

import digest.main  # noqa: F401 -- initializes generated Qt UI import paths
from digest.folder_scan import FolderScanThread
from digest.freeze_inputs import FreezeInputs
from digest.logging_utils import LogStream
from digest.multi_model_selection_page import MultiModelSelectionPage
from digest.similarity_analysis import SimilarityWorker


@pytest.fixture(scope="module")
def app():
    application = QApplication.instance() or QApplication([])
    application.setQuitOnLastWindowClosed(False)
    yield application


def dynamic_model():
    return onnx.helper.make_model(
        onnx.helper.make_graph(
            [onnx.helper.make_node("Relu", ["x"], ["y"])], "dynamic",
            [onnx.helper.make_tensor_value_info("x", onnx.TensorProto.FLOAT, ["batch", 2])],
            [onnx.helper.make_tensor_value_info("y", onnx.TensorProto.FLOAT, ["batch", 2])],
        ),
        opset_imports=[onnx.helper.make_opsetid("", 17)], ir_version=10,
    )


@pytest.fixture
def freeze(app, tmp_path):  # noqa: ARG001 -- QApplication must exist before constructing widgets
    with patch("digest.freeze_inputs.user_cache_dir", return_value=str(tmp_path)):
        widget = FreezeInputs(dynamic_model(), "dynamic")
    yield widget
    widget.close()


def dimension_field(widget):
    return widget.ui.formLayout.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()


@pytest.mark.parametrize("text", ["", "abc", "0", "-1", "1.5", str(2**63)])
def test_invalid_dimensions_cannot_be_applied(freeze, text, tmp_path):
    dimension_field(freeze).setText(text)
    assert not freeze.ui.applyShapesBtn.isEnabled()
    freeze.apply_static_shapes()
    assert list(tmp_path.glob("*.onnx")) == []


def test_inference_failure_can_be_corrected_and_retried(freeze, tmp_path):
    original = freeze.model_proto.SerializeToString()
    emitted = []
    freeze.complete_signal.connect(emitted.append)
    dimension_field(freeze).setText("2")
    with patch(
        "digest.freeze_inputs.shape_inference.infer_shapes",
        side_effect=onnx.shape_inference.InferenceError("bad shape"),
    ):
        freeze.apply_static_shapes()
    assert "bad shape" in freeze.ui.selectDirLabel.text()
    assert freeze.ui.applyShapesBtn.isEnabled()
    assert emitted == []
    assert list(tmp_path.glob("*.onnx")) == []
    dimension_field(freeze).setText("3")
    freeze.apply_static_shapes()
    assert len(emitted) == 1
    result = onnx.load(emitted[0])
    onnx.checker.check_model(result, full_check=True)
    assert result.graph.input[0].type.tensor_type.shape.dim[0].dim_value == 3
    assert freeze.model_proto.SerializeToString() == original


def test_cancel_freeze_never_saves_or_emits(freeze):
    dimension_field(freeze).setText("2")
    emitted = []
    freeze.complete_signal.connect(emitted.append)
    progress = MagicMock()
    progress.wasCanceled.return_value = True
    with patch("digest.freeze_inputs.ProgressDialog", return_value=progress), patch(
        "digest.freeze_inputs.save"
    ) as save:
        freeze.apply_static_shapes()
    save.assert_not_called()
    progress.close.assert_called_once()
    assert emitted == []
    assert freeze.ui.applyShapesBtn.isEnabled()


def test_save_failure_keeps_freeze_retry_available(freeze):
    dimension_field(freeze).setText("2")
    emitted = []
    freeze.complete_signal.connect(emitted.append)
    with patch("digest.freeze_inputs.save", side_effect=OSError("disk full")):
        freeze.apply_static_shapes()
    assert "disk full" in freeze.ui.selectDirLabel.text()
    assert freeze.ui.applyShapesBtn.isEnabled()
    assert emitted == []


def test_folder_scan_groups_duplicates_and_skips_bad_files(tmp_path):
    onnx.save(dynamic_model(), tmp_path / "one.onnx")
    onnx.save(dynamic_model(), tmp_path / "two.onnx")
    (tmp_path / "broken.onnx").write_bytes(b"not an onnx model")
    (tmp_path / "unrelated.yaml").write_text("setting: true", encoding="utf-8")
    source = Path(__file__).parent / "resnet18_reports" / "resnet18_report.yaml"
    report = yaml.safe_load(source.read_text(encoding="utf-8"))
    (tmp_path / "a.yaml").write_text(yaml.safe_dump(report), encoding="utf-8")
    report["model_file"] = "another/location.onnx"
    report["report_date"] = "another date"
    (tmp_path / "b.yaml").write_text(yaml.safe_dump(report), encoding="utf-8")
    with patch("digest.folder_scan.psutil.virtual_memory", return_value=MagicMock(percent=10)):
        result = FolderScanThread(str(tmp_path)).scan()
    assert sorted(map(len, result["groups"])) == [2, 2]
    assert result["errors"] == 1
    assert not result["limited"]


def test_folder_scan_obeys_memory_limit(tmp_path):
    onnx.save(dynamic_model(), tmp_path / "one.onnx")
    with patch("digest.folder_scan.psutil.virtual_memory", return_value=MagicMock(percent=95)):
        result = FolderScanThread(str(tmp_path)).scan()
    assert result["limited"]
    assert result["groups"] == []


def wait_until(app, predicate):
    deadline = time.monotonic() + 5
    while not predicate() and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.005)
    assert predicate()


def test_folder_scan_keeps_gui_responsive_and_can_be_canceled(app, tmp_path):
    onnx.save(dynamic_model(), tmp_path / "one.onnx")
    entered = threading.Event()
    release = threading.Event()
    load = onnx.load

    def slow_load(*args, **kwargs):
        entered.set()
        assert release.wait(5)
        return load(*args, **kwargs)

    page = MultiModelSelectionPage()
    try:
        with patch("digest.folder_scan.onnx.load", side_effect=slow_load), patch(
            "digest.folder_scan.psutil.virtual_memory", return_value=MagicMock(percent=10)
        ):
            page.set_directory(str(tmp_path))
            wait_until(app, entered.is_set)
            assert not page.ui.selectFolderBtn.isEnabled()
            page.scan_thread.requestInterruption()
            app.processEvents()
            release.set()
            wait_until(app, lambda: page.scan_thread is None)
        assert page.item_model.rowCount() == 0
        assert page.ui.selectFolderBtn.isEnabled()
        assert "canceled" in page.ui.infoLabel.text()
    finally:
        release.set()
        page.stop_workers()
        page.close()


def test_similarity_failure_still_emits_completion():
    worker = SimilarityWorker("bad.onnx", "heatmap.png", "model-id")
    results = []
    worker.signals.completed.connect(lambda *args: results.append(args))
    with patch("digest.similarity_analysis.find_match", side_effect=OSError("unreadable")):
        worker.run()
    assert len(results) == 1
    assert results[0][0] is False
    assert results[0][4].empty


def test_windowed_output_is_logged_and_buffer_is_bounded(caplog):
    stream = LogStream(None, logging.ERROR)
    with caplog.at_level(logging.ERROR, logger="digest.console"):
        stream.write("first")
        stream.write(" message\n")
        stream.write("x" * 8192)
        stream.flush()
    assert "first message" in caplog.text
    assert stream.pending == ""


def test_logging_captures_output_and_uncaught_exceptions(tmp_path):
    code = """
import sys
from pathlib import Path
from unittest.mock import patch
from digest.logging_utils import configure_logging
with patch('digest.logging_utils.log_path', return_value=Path(sys.argv[1])):
    configure_logging()
print('stdout diagnostic')
sys.stderr.write('stderr diagnostic\\n')
raise RuntimeError('uncaught diagnostic')
"""
    logfile = tmp_path / "digest.log"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-c", code, str(logfile)], env=env, capture_output=True, timeout=30, check=False,
    )
    assert result.returncode != 0
    text = logfile.read_text(encoding="utf-8")
    assert "stdout diagnostic" in text
    assert "stderr diagnostic" in text
    assert "RuntimeError: uncaught diagnostic" in text
