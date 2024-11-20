# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
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
