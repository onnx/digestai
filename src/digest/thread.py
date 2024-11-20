# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

# pylint: disable=no-name-in-module
import os
from typing import Optional
from PySide6.QtCore import QThread, Signal
from utils import onnx_utils
from digest.subgraph_analysis.find_match import find_match


class StatsThread(QThread):

    completed = Signal(onnx_utils.DigestOnnxModel, str)

    def __init__(
        self,
        model=None,
        tab_name: Optional[str] = None,
        unique_id: Optional[str] = None,
    ):
        super().__init__()
        self.model = model
        self.tab_name = tab_name
        self.unique_id = unique_id

    def run(self):
        if not self.model:
            raise ValueError("You must specify a model.")
        if not self.tab_name:
            raise ValueError("You must specify a tab name.")
        if not self.unique_id:
            raise ValueError("You must specify a unique id.")

        digest_model = onnx_utils.DigestOnnxModel(self.model, save_proto=False)

        self.completed.emit(digest_model, self.unique_id)


class SimilarityThread(QThread):

    completed_successfully = Signal(bool, str, str, str)

    def __init__(
        self,
        model_filepath: Optional[str] = None,
        png_filepath: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        super().__init__()
        self.model_filepath = model_filepath
        self.png_filepath = png_filepath
        self.model_id = model_id

    def run(self):
        if not self.model_filepath:
            raise ValueError("You must set the model filepath")
        if not self.png_filepath:
            raise ValueError("You must set the png filepath")
        if not self.model_id:
            raise ValueError("You must set the model id")

        try:
            most_similar, _ = find_match(
                self.model_filepath,
                self.png_filepath,
                dequantize=False,
                replace=True,
                dark_mode=True,
            )
            most_similar = [os.path.basename(path) for path in most_similar]
            most_similar = ",".join(most_similar[1:4])
            self.completed_successfully.emit(
                True, self.model_id, most_similar, self.png_filepath
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            most_similar = ""
            self.completed_successfully.emit(
                False, self.model_id, most_similar, self.png_filepath
            )
            print(f"Issue creating similarity analysis: {e}")
