# pylint: disable=no-name-in-module
# Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt


class ClickableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked = None  # Store a reference to the callback function

    def set_click_callback(self, callback):
        self.clicked = callback

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.clicked is not None:
            self.clicked()  # Call the callback function
