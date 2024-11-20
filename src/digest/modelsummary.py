# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os

# pylint: disable=invalid-name
from typing import Optional

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget

from onnx import ModelProto

from digest.ui.modelsummary_ui import Ui_modelSummary
from digest.freeze_inputs import FreezeInputs
from digest.popup_window import PopupWindow
from digest.qt_utils import apply_dark_style_sheet
from utils import onnx_utils

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class modelSummary(QWidget):

    def __init__(self, digest_model: onnx_utils.DigestOnnxModel, parent=None):
        super().__init__(parent)
        self.ui = Ui_modelSummary()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)

        self.file: Optional[str] = None
        self.ui.freezeButton.setVisible(False)
        self.ui.freezeButton.clicked.connect(self.open_freeze_inputs)
        self.ui.warningLabel.hide()
        self.digest_model = digest_model
        self.model_proto: ModelProto = (
            digest_model.model_proto if digest_model.model_proto else ModelProto()
        )
        model_name: str = digest_model.model_name if digest_model.model_name else ""
        self.freeze_inputs = FreezeInputs(self.model_proto, model_name)
        self.freeze_inputs.complete_signal.connect(self.close_freeze_window)
        self.freeze_window: Optional[QWidget] = None

    def open_freeze_inputs(self):
        self.freeze_window = PopupWindow(
            self.freeze_inputs, "Freeze Model Inputs", self
        )
        self.freeze_window.open()

    def close_freeze_window(self):
        if self.freeze_window:
            self.freeze_window.close()
