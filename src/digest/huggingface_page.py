# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

from typing import Dict, Optional
import logging

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget
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
from digest.dialog import ProgressDialog

logger = logging.getLogger("huggingface_hub")
logger.setLevel(logging.INFO)


class SearchSignals(QObject):
    completed = Signal(dict, str)  # Changed to emit processed data directly
    started = Signal(str)  # Signal to indicate search has started


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

        # Signal that search has started
        self.signals.started.emit(self.search_text)

        # First, search for models
        if "huggingface.co/" in self.search_text:
            search_text = self.search_text.split("huggingface.co/")[-1]
            hf_models = [hf_api.model_info(repo_id=search_text)]
        else:
            hf_models = list(
                hf_api.list_models(search=self.search_text, library="onnx")
            )

        # Then, process the models to get their files
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

        # Emit the processed data directly
        self.signals.completed.emit(column_data, self.search_text)


class DownloadSignal(QObject):
    progress = Signal(int)  # Signal to emit the download progress (0-100)
    finished = Signal(str)
    started = Signal(str)  # Signal to indicate download has started


class HFDownloadThread(QThread):
    def __init__(self, repo_id, filename):
        super().__init__()
        self.repo_id = repo_id
        self.filename = filename
        self.signals = DownloadSignal()

    def run(self):
        self.signals.started.emit(self.filename)

        try:
            # Download the file
            path = hf_hub_download(
                self.repo_id, filename=self.filename, force_download=True
            )

            # Signal completion
            self.signals.finished.emit(path)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error downloading file: {e}")
            self.signals.finished.emit("")  # Empty string indicates error


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

        self.download_progress_dialog = None
        self.search_progress_dialog = None

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
        search_text = self.ui.hf_search_text.toPlainText().strip()
        if not search_text:
            return

        # Create and configure the search thread
        self.search_thread = HFSearchThread(search_text)
        self.search_thread.signals.started.connect(self.on_search_started)
        self.search_thread.signals.completed.connect(self.on_search_completed)

        # Start the search thread
        self.search_thread.start()

    def on_search_started(self, search_text):
        # Create indeterminate progress dialog for search
        self.search_progress_dialog = ProgressDialog(
            f"Searching for '{search_text}'", 0, self
        )
        self.search_progress_dialog.setWindowTitle("Searching Huggingface")
        self.search_progress_dialog.setMinimum(0)
        self.search_progress_dialog.setMaximum(0)  # Makes it indeterminate

        # Connect cancel button
        self.search_progress_dialog.canceled.connect(self.cancel_search)

        # Show the dialog
        self.search_progress_dialog.show()

        # Update message
        self.update_message_label(info_message="Searching huggingface...")

    def on_search_completed(self, column_data, search_text):
        # Close the progress dialog
        if self.search_progress_dialog:
            self.search_progress_dialog.close()
            self.search_progress_dialog = None

        # Update the UI with the processed data
        self.update_model_list_view(column_data, search_text)

    def cancel_search(self):
        if self.search_thread and self.search_thread.isRunning():
            # Terminate the search thread
            self.search_thread.terminate()
            self.search_thread.wait()
            self.update_message_label(info_message="Search canceled")

        # Close the progress dialog if it's open
        if self.search_progress_dialog:
            self.search_progress_dialog.close()
            self.search_progress_dialog = None

    def update_model_list_view(self, column_data, search_text):
        """Update the UI with the processed model data"""
        model = QStandardItemModel()

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

        if not column_data:
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

        # Create progress dialog without steps (indeterminate)
        self.download_progress_dialog = ProgressDialog(
            f"Downloading {onnx_file}", 0, self
        )
        self.download_progress_dialog.setWindowTitle("Downloading Model")
        self.download_progress_dialog.setMinimum(0)
        self.download_progress_dialog.setMaximum(0)

        # Connect signals
        self.download_thread.signals.started.connect(
            lambda filename: self.download_progress_dialog.show()
        )

        self.download_thread.signals.finished.connect(
            lambda path: (
                (
                    self.currently_selected_hf_onnx.update({"cache": path})
                    if path
                    else None
                ),
                self.download_progress_dialog.close(),
                self.model_signal.emit(path) if path else None,
                self.update_message_label(
                    info_message=(
                        f"Downloaded model to {path}" if path else "Download failed"
                    )
                ),
            )
        )

        # Handle cancel button in progress dialog
        self.download_progress_dialog.canceled.connect(self.cancel_download)

        self.download_thread.start()

    def cancel_download(self):
        if self.download_thread and self.download_thread.isRunning():
            # Terminate the download thread
            self.download_thread.terminate()
            self.download_thread.wait()
            self.update_message_label(info_message="Download canceled")
