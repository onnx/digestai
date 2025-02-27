# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

# pylint: disable=no-name-in-module
import os
from typing import List, Optional
from PySide6.QtCore import Signal, QRunnable, QObject
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from digest.subgraph_analysis.find_match import find_match


class WorkerSignals(QObject):
    completed = Signal(bool, str, str, str, pd.DataFrame)


class SimilarityWorker(QRunnable):

    def __init__(
        self,
        model_file_path: Optional[str] = None,
        png_file_path: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        super().__init__()
        self.signals = WorkerSignals()
        self.model_filepath = model_file_path
        self.png_filepath = png_file_path
        self.model_id = model_id

    def run(self):
        if not self.model_filepath:
            raise ValueError("You must set the model filepath")
        if not self.png_filepath:
            raise ValueError("You must set the png filepath")
        if not self.model_id:
            raise ValueError("You must set the model id")

        try:
            most_similar, _, df_sorted = find_match(
                self.model_filepath,
                dequantize=False,
                replace=True,
            )
            most_similar = [os.path.basename(path) for path in most_similar]
            # We convert List[str] to str to send through the signal
            most_similar = ",".join(most_similar)
            self.signals.completed.emit(
                True, self.model_id, most_similar, self.png_filepath, df_sorted
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            most_similar = ""
            self.signals.completed.emit(
                False, self.model_id, most_similar, self.png_filepath, df_sorted
            )
            print(f"Issue creating similarity analysis: {e}")


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
