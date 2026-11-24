# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

from PySide6.QtWidgets import (
    QPlainTextEdit,
)
from PySide6.QtGui import (
    QKeyEvent,
)
from PySide6.QtCore import (
    Signal,
    Qt,
)


class PlainTextEditEnterSignal(QPlainTextEdit):
    returnPressed = Signal()  # Custom signal

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.returnPressed.emit()  # Emit a custom signal
        else:
            super().keyPressEvent(event)  # Handle other key presses normally
