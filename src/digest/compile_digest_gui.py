# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import subprocess

DIGEST_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
QRC_FILE_PATH = os.path.join(DIGEST_DIRECTORY, "resource.qrc")
UI_DIRECTORY = os.path.join(DIGEST_DIRECTORY, "ui")


def compile_ui_files(directory: str) -> None:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ui"):
                ui_path = os.path.join(root, file)
                py_path = os.path.splitext(ui_path)[0] + "_ui.py"

                try:
                    subprocess.run(["pyside6-uic", ui_path, "-o", py_path], check=True)
                    print(f"Compiled: {ui_path} -> {py_path}")
                except subprocess.CalledProcessError:
                    print(f"Error compiling: {ui_path}")


def compile_rcc_file(qrc_file_path: str) -> None:
    py_path = os.path.splitext(qrc_file_path)[0] + "_rc.py"
    try:
        subprocess.run(["pyside6-rcc", qrc_file_path, "-o", py_path], check=True)
        print(f"Compiled: {qrc_file_path} -> {py_path}")
    except subprocess.CalledProcessError:
        print(f"Error compiling: {qrc_file_path}")


if __name__ == "__main__":
    compile_rcc_file(QRC_FILE_PATH)
    compile_ui_files(UI_DIRECTORY)
