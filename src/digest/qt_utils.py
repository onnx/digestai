# Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.

import os
from typing import List, Union, Optional
import psutil

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QFile, QTextStream

from digest.dialog import StatusDialog

ROOT_FOLDER = os.path.dirname(__file__)
BASE_STYLE_FILE = os.path.join(ROOT_FOLDER, "styles", "darkstyle.qss")


def get_ram_utilization() -> float:
    mem = psutil.virtual_memory()
    ram_util_perc = mem.percent
    return ram_util_perc


def prompt_user_ram_limit(
    sys_ram_percent_limit: float = 90.0,
    message: Optional[str] = None,
    parent: Optional[QWidget] = None,
) -> bool:
    current_ram_util = get_ram_utilization()
    if current_ram_util >= sys_ram_percent_limit:
        if not message:
            message = f"System RAM utilization is at {current_ram_util}."
        dialog = StatusDialog(message, parent=parent)
        dialog.show()
        return True
    return False


def apply_style_sheet(widget: Union[QWidget, QApplication], style_path: str) -> None:

    if not os.path.exists(style_path):
        raise FileExistsError(f"File {style_path} not found.")

    style_qfile = QFile(style_path)
    style_qfile.open(QFile.ReadOnly | QFile.Text)  # type: ignore
    style_stream = QTextStream(style_qfile).readAll()
    widget.setStyleSheet(style_stream)


def apply_dark_style_sheet(widget: Union[QWidget, QApplication]) -> None:
    apply_style_sheet(widget, BASE_STYLE_FILE)


def apply_multiple_style_sheets(
    widget: Union[QWidget, QApplication], style_file_paths: List[str]
) -> None:

    style_stream = ""

    for style_path in style_file_paths:
        if not os.path.exists(style_path):
            raise FileExistsError(f"File {style_path} not found.")

        style_qfile = QFile(style_path)
        style_qfile.open(QFile.ReadOnly | QFile.Text)  # type: ignore
        style_stream += QTextStream(style_qfile).readAll()

    widget.setStyleSheet(style_stream)


def find_available_save_path(save_path: str) -> str:
    """Increments a counter until it finds a suitable save location
    For example, if my/dir already exists this function will return the first
    available location out of my/dir(1) or my/dir(2) etc..."""
    counter = 1
    new_path = save_path
    while os.path.exists(new_path):
        base_dir, base_name = os.path.split(save_path)
        name, ext = os.path.splitext(base_name)
        new_path = os.path.join(base_dir, f"{name}({counter}){ext}")
        counter += 1
    return new_path
