# Copyright (c) ONNX Project Contributors
# SPDX-License-Identifier: Apache-2.0

"""Discover and group model files without touching GUI widgets."""

import hashlib
import logging
import os

import onnx
import psutil
import yaml
from PySide6.QtCore import QThread, Signal

from digest.model_class.digest_report_model import validate_yaml

LOGGER = logging.getLogger(__name__)
REPORT_METADATA = {"report_date", "model_file", "model_files", "digest_version"}


def report_contents(value):
    if isinstance(value, dict):
        return {key: report_contents(item) for key, item in value.items() if key not in REPORT_METADATA}
    if isinstance(value, list):
        return [report_contents(item) for item in value]
    return value


class FolderScanThread(QThread):
    completed = Signal(dict)
    failed = Signal(str)
    canceled = Signal()
    progress = Signal(str)

    def __init__(self, directory, parent=None):
        super().__init__(parent)
        self.directory = directory

    def run(self):
        try:
            result = self.scan()
        except Exception as error:  # noqa: BLE001 -- deliver worker failures to the GUI
            LOGGER.exception("Could not scan folder %s", self.directory)
            self.failed.emit(str(error))
        else:
            if result is None:
                self.canceled.emit()
            else:
                self.completed.emit(result)

    def scan(self):
        groups = {}
        total = 0
        errors = 0
        limited = False

        def walk_error(error):
            nonlocal errors
            errors += 1
            LOGGER.warning("Cannot scan directory: %s", error)

        for directory, directories, filenames in os.walk(self.directory, onerror=walk_error):
            if self.isInterruptionRequested():
                return None
            directories.sort()
            for filename in sorted(filenames):
                if self.isInterruptionRequested():
                    return None
                extension = os.path.splitext(filename)[1].lower()
                if extension not in {".onnx", ".yaml"}:
                    continue
                total += 1
                if total % 50 == 1:
                    self.progress.emit(f"Scanning model file {total}...")
                if psutil.virtual_memory().percent >= 90:
                    limited = True
                    break
                path = os.path.normpath(os.path.join(directory, filename))
                try:
                    if extension == ".onnx":
                        model = onnx.load(path, load_external_data=False)
                        signature = hashlib.sha256(model.SerializeToString()).digest()
                        del model
                    else:
                        if not validate_yaml(path):
                            continue
                        with open(path, encoding="utf-8") as file:
                            report = report_contents(yaml.safe_load(file))
                        signature = hashlib.sha256(yaml.safe_dump(report, sort_keys=True).encode()).digest()
                    groups.setdefault((extension, signature), []).append(path)
                except Exception:  # noqa: BLE001 -- skip a malformed file and continue the scan
                    errors += 1
                    LOGGER.exception("Skipping unreadable model %s", path)
            if limited:
                break
        if self.isInterruptionRequested():
            return None
        return {"groups": list(groups.values()), "total": total, "errors": errors, "limited": limited}
