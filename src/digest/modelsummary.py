# Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.

import os

# pylint: disable=invalid-name
from typing import Optional, Union

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QMovie
from PySide6.QtCore import QSize

from onnx import ModelProto

from digest.ui.modelsummary_ui import Ui_modelSummary
from digest.freeze_inputs import FreezeInputs
from digest.popup_window import PopupWindow
from digest.qt_utils import apply_dark_style_sheet
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.model_class.digest_report_model import DigestReportModel


ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class modelSummary(QWidget):

    def __init__(
        self, digest_model: Union[DigestOnnxModel, DigestReportModel], parent=None
    ):
        super().__init__(parent)
        self.ui = Ui_modelSummary()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)

        self.file: Optional[str] = None
        self.ui.warningLabel.hide()
        self.digest_model = digest_model
        self.model_proto: Optional[ModelProto] = None
        model_name: str = digest_model.model_name if digest_model.model_name else ""

        self.load_gif = QMovie(":/assets/gifs/load.gif")
        # We set the size of the GIF to half the original
        self.load_gif.setScaledSize(QSize(214, 120))
        self.ui.similarityImg.setMovie(self.load_gif)
        self.load_gif.start()

        # There is no freezing if the model is not ONNX
        self.ui.freezeButton.setVisible(False)
        self.freeze_inputs: Optional[FreezeInputs] = None
        self.freeze_window: Optional[QWidget] = None

        if isinstance(digest_model, DigestOnnxModel):
            self.model_proto = (
                digest_model.model_proto if digest_model.model_proto else ModelProto()
            )
            self.freeze_inputs = FreezeInputs(self.model_proto, model_name)
            self.ui.freezeButton.clicked.connect(self.open_freeze_inputs)
            self.freeze_inputs.complete_signal.connect(self.close_freeze_window)

    def open_freeze_inputs(self):
        if self.freeze_inputs:
            self.freeze_window = PopupWindow(
                self.freeze_inputs, "Freeze Model Inputs", self
            )
            self.freeze_window.open()

    def close_freeze_window(self):
        if self.freeze_window:
            self.freeze_window.close()
