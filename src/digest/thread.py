# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

# pylint: disable=no-name-in-module
import os
from typing import List, Optional
from PySide6.QtCore import QThread, Signal, QEventLoop, QTimer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.subgraph_analysis.find_match import find_match


def wait_threads(threads: List[QThread], timeout=10000) -> bool:

    loop = QEventLoop()
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(loop.quit)

    def check_threads():
        if all(thread.isFinished() for thread in threads):
            loop.quit()

    check_timer = QTimer()
    check_timer.timeout.connect(check_threads)
    check_timer.start(100)  # Check every 100ms

    timer.start(timeout)
    loop.exec()

    check_timer.stop()
    timer.stop()

    # Return True if all threads finished, False if timed out
    return all(thread.isFinished() for thread in threads)


class StatsThread(QThread):

    completed = Signal(DigestOnnxModel, str)

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

        digest_model = DigestOnnxModel(self.model, save_proto=False)

        self.completed.emit(digest_model, self.unique_id)

    def wait(self, timeout=10000):
        wait_threads([self], timeout)


class SimilarityThread(QThread):

    completed_successfully = Signal(bool, str, str, str, pd.DataFrame)

    def __init__(
        self,
        model_file_path: Optional[str] = None,
        png_file_path: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        super().__init__()
        self.model_file_path = model_file_path
        self.png_file_path = png_file_path
        self.model_id = model_id

    def run(self):
        if not self.model_file_path:
            raise ValueError("You must set the model file_path")
        if not self.png_file_path:
            raise ValueError("You must set the png file_path")
        if not self.model_id:
            raise ValueError("You must set the model id")

        try:
            most_similar, _, df_sorted = find_match(
                self.model_file_path,
                dequantize=False,
                replace=True,
            )
            most_similar = [os.path.basename(path) for path in most_similar]
            # We convert List[str] to str to send through the signal
            most_similar = ",".join(most_similar)
            self.completed_successfully.emit(
                True, self.model_id, most_similar, self.png_file_path, df_sorted
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            most_similar = ""
            self.completed_successfully.emit(
                False, self.model_id, most_similar, self.png_file_path, df_sorted
            )
            print(f"Issue creating similarity analysis: {e}")

    def wait(self, timeout=10000):
        wait_threads([self], timeout)


def post_process(
    model_name: str,
    name_list: List[str],
    df_sorted: pd.DataFrame,
    png_file_path: str,
    dark_mode: bool = True,
):
    """Matplotlib is not thread safe so we must do post_processing on the main thread"""
    if dark_mode:
        plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(df_sorted, cmap="viridis")

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(df_sorted.columns)))
    ax.set_yticks(np.arange(len(name_list)))
    ax.set_xticklabels([a[:5] for a in df_sorted.columns])
    ax.set_yticklabels(name_list)

    # Rotate the tick labels and set their alignment
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    ax.set_title(f"Model Similarity Heatmap - {model_name}")

    cb = plt.colorbar(
        im,
        ax=ax,
        shrink=0.5,
        format="%.2f",
        label="Correlation Ratio",
        orientation="vertical",
        # pad=0.02,
    )
    cb.set_ticks([0, 0.5, 1])  # Set colorbar ticks at 0, 0.5, and 1
    cb.set_ticklabels(
        ["0.0 (Low)", "0.5 (Medium)", "1.0 (High)"]
    )  # Set corresponding labels
    cb.set_label("Correlation Ratio", labelpad=-100)

    fig.tight_layout()

    if png_file_path is None:
        png_file_path = "heatmap.png"

    fig.savefig(png_file_path)

    plt.close(fig)
