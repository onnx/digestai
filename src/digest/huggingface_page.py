# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

from typing import Dict, Optional, List
import logging

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
)
from PySide6.QtCore import (
    Signal,
    QObject,
    QThread,
    Qt,
)
from huggingface_hub import hf_api, hf_hub_download
from huggingface_hub.hf_api import ModelInfo
from digest.ui.huggingface_page_ui import Ui_huggingfacePage

logger = logging.getLogger("huggingface_hub")
logger.setLevel(logging.INFO)


class SearchSignals(QObject):
    completed = Signal(list, str)


class HFSearchThread(QThread):
    def __init__(
        self,
        search_text: Optional[str] = None,
    ):
        super().__init__()
        self.signals = SearchSignals()
        self.search_text = search_text

    def run(self):
        if not self.search_text:
            raise ValueError("Search text is not set.")

        if "huggingface.co/" in self.search_text:
            search_text = self.search_text.split("huggingface.co/")[-1]
            hf_models = [hf_api.model_info(repo_id=search_text)]
        else:
            hf_models = list(
                hf_api.list_models(search=self.search_text, library="onnx")
            )

        self.signals.completed.emit(hf_models, self.search_text)


class DownloadSignal(QObject):
    progress = Signal(int)  # Signal to emit the download progress (0-100)
    finished = Signal(str)


class HFDownloadThread(QThread):
    def __init__(self, repo_id, filename):
        super().__init__()
        self.repo_id = repo_id
        self.filename = filename
        self.signals = DownloadSignal()

    def run(self):
        path = hf_hub_download(self.repo_id, filename=self.filename)
        self.signals.finished.emit(path)


class HuggingfacePage(QWidget):

    model_signal = Signal(ModelInfo)

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_huggingfacePage()
        self.ui.setupUi(self)
        self.default_state()

        self.currently_selected_hf_onnx: Dict[str, Optional[str]] = {}
        self.currently_selected_hf_onnx["repo_id"] = None
        self.currently_selected_hf_onnx["onnx_file"] = None
        self.currently_selected_hf_onnx["cache"] = None

        self.ui.hf_search_text.returnPressed.connect(self.ui.hf_search_btn.click)
        self.ui.hf_search_btn.clicked.connect(self.on_search_btn_clicked)
        self.ui.open_onnx_btn.clicked.connect(self.download_hf_onnx_model)

        self.search_thread = None
        self.download_thread = None

    def update_message_label(
        self, info_message: Optional[str] = None, warn_message: Optional[str] = None
    ) -> None:
        if info_message:
            message = f"ℹ️ {info_message}"
        elif warn_message:
            message = f"⚠️ {warn_message}"

        self.ui.hf_info_label.setText(message)

    def default_state(self):
        self.update_message_label(
            info_message="Search above for ONNX files stored on Huggingface repos."
        )

    def on_column_view_selection_change(self, selected):
        index = selected.indexes()[0]
        onnx_file = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if onnx_file.endswith(".onnx"):
            self.ui.open_onnx_btn.setEnabled(True)  # Enable the button
            self.currently_selected_hf_onnx["onnx_file"] = onnx_file
            parent_index = index.parent()
            if parent_index.isValid():
                # Get the text of the parent item
                self.currently_selected_hf_onnx["repo_id"] = index.model().data(
                    parent_index, Qt.ItemDataRole.DisplayRole
                )
            return

        self.ui.open_onnx_btn.setEnabled(False)
        self.currently_selected_hf_onnx["repo_id"] = None
        self.currently_selected_hf_onnx["onnx_file"] = None
        self.currently_selected_hf_onnx["cache"] = None

    def get_selected_leaf_text(self):
        selection_model = self.ui.hf_column_view.selectionModel()
        if selection_model.hasSelection():
            index = selection_model.currentIndex()
            if not index.model().hasChildren(index):
                return index.model().data(index, Qt.ItemDataRole.DisplayRole)
        return None  # Return None if no leaf is selected

    def on_search_btn_clicked(self):
        QApplication.processEvents()  # ensure the label is updated before the api call
        search_text = self.ui.hf_search_text.toPlainText().strip()
        if not search_text:
            return

        self.update_message_label(info_message="Searching huggingface...")
        self.search_thread = HFSearchThread(search_text)
        self.search_thread.signals.completed.connect(self.list_hf_models)
        self.search_thread.search_text = search_text
        self.search_thread.start()

    def list_hf_models(self, hf_models: List[ModelInfo], search_text: str):

        model = QStandardItemModel()
        column_data = {}
        for hf_model in hf_models:
            column_data[hf_model.id] = {
                "onnx": [],
                "url": hf_model.id,
            }
            try:
                all_repo_files = hf_api.list_repo_files(hf_model.id)
                all_onnx_files = [f for f in all_repo_files if f.endswith(".onnx")]
                for onnx_file in all_onnx_files:
                    column_data[hf_model.id]["onnx"].append(onnx_file)
            except hf_api.HTTPError as err:
                column_data[hf_model.id]["onnx"].append("Error accessing repo")
                print(f"Error accessing model {hf_model}: {err}")
                continue

        parentItem = model.invisibleRootItem()
        for model_name, model_details in column_data.items():
            item = QStandardItem(model_name)
            parentItem.appendRow(item)
            for onnx_file in model_details["onnx"]:
                childItem = QStandardItem(onnx_file)
                item.appendRow(childItem)

        self.ui.hf_column_view.setModel(model)
        self.ui.hf_column_view.selectionModel().selectionChanged.connect(
            self.on_column_view_selection_change
        )

        if not hf_models:
            self.update_message_label(
                warn_message=f"No ONNX models were found from searching {search_text}"
            )
        else:
            self.update_message_label(
                info_message=f"Search results shown for {search_text} below"
            )

    def download_hf_onnx_model(self):
        repo_id = self.currently_selected_hf_onnx["repo_id"]
        onnx_file = self.currently_selected_hf_onnx["onnx_file"]
        if not repo_id or not onnx_file or not onnx_file.endswith(".onnx"):
            return

        self.update_message_label(info_message=f"Downloading model {onnx_file}")

        self.download_thread = HFDownloadThread(repo_id, onnx_file)

        self.download_thread.signals.finished.connect(
            lambda path: (
                self.currently_selected_hf_onnx.update({"cache": path}),
                self.model_signal.emit(path),
                self.update_message_label(info_message=f"Downloaded model to {path}"),
            )
        )

        self.download_thread.start()
