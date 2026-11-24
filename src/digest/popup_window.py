# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QIcon


class PopupWindow(QWidget):
    def __init__(self, widget: QWidget, window_title: str = "", parent=None):
        super().__init__(parent)

        self.main_window = QMainWindow()
        self.main_window.setCentralWidget(widget)
        self.main_window.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))
        self.main_window.setWindowTitle(window_title)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.main_window.resize(
            int(screen_geometry.width() / 1.5), int(screen_geometry.height() * 0.80)
        )

    def open(self):
        self.main_window.show()

    def close(self):
        self.main_window.close()


class PopupDialog(QDialog):
    """Open a modal child window and wait until its content closes it."""

    def __init__(self, widget: QWidget, window_title: str = "", parent=None):
        super().__init__(parent)

        if hasattr(widget, "close_signal"):
            widget.close_signal.connect(self.close)

        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowFlags(Qt.WindowType.Window)

        layout = QVBoxLayout()
        layout.addWidget(widget)
        self.setLayout(layout)

        self.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))
        self.setWindowTitle(window_title)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.resize(
            int(screen_geometry.width() / 1.5), int(screen_geometry.height() * 0.80)
        )

    def open(self):
        self.show()
        self.exec()
