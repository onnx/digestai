# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
from typing import List, Optional, Dict, Union

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QMenu,
    QApplication,
    QFileDialog,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QIcon
from PySide6.QtCore import Qt, Signal, QThread

from digest.dialog import WarnDialog, ProgressDialog
from digest.ui.multimodelselection_page_ui import Ui_MultiModelSelection
from digest.multi_model_analysis import MultiModelAnalysis
from digest.qt_utils import apply_dark_style_sheet
from digest.folder_scan import FolderScanThread
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.model_class.digest_report_model import DigestReportModel
from utils import onnx_utils


class AnalysisThread(QThread):
    open_progress = Signal(str, int)  # Signal to open dialog
    step_progress = Signal()  # Signal to send progress value
    close_progress = Signal()  # Signal to close dialog
    completed = Signal(list)  # Signal for thread completion

    def __init__(self):
        super().__init__()
        self.model_dict: Dict[
            str, Optional[Union[DigestOnnxModel, DigestReportModel]]
        ] = {}
        self.user_canceled = False

    def run(self):
        # We perform the initial model analysis here so that we can cache the result in case
        # the user closes the window and re-opens it.
        self.open_progress.emit("Performing model analysis", len(self.model_dict))

        for file, model in self.model_dict.items():
            if self.user_canceled:
                self.close_progress.emit()
                self.completed.emit([])
                return
            self.step_progress.emit()
            if model:
                continue
            model_name, file_ext = os.path.splitext(os.path.basename(file))
            if file_ext == ".onnx":
                model_proto = onnx_utils.load_onnx(file, False)
                self.model_dict[file] = DigestOnnxModel(
                    model_proto,
                    onnx_filepath=file,
                    model_name=model_name,
                    save_proto=False,
                )
            elif file_ext == ".yaml":
                self.model_dict[file] = DigestReportModel(file)

        self.close_progress.emit()

        model_list = list(self.model_dict.values())

        self.completed.emit(model_list)

    def stop_processing(self) -> None:
        self.user_canceled = True


class MultiModelSelectionPage(QWidget):

    model_signal = Signal(str)

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_MultiModelSelection()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)
        self.ui.warningLabel.hide()
        self.item_model = QStandardItemModel()
        self.item_model.itemChanged.connect(self.update_num_selected_label)
        self.ui.radioAll.setChecked(True)
        self.ui.radioAll.toggled.connect(self.update_list_view_items)
        self.ui.radioONNX.toggled.connect(self.update_list_view_items)
        self.ui.radioReports.toggled.connect(self.update_list_view_items)
        self.ui.selectFolderBtn.clicked.connect(self.openFolder)

        # We want to retain the size when the duplicate label
        # is hidden to keep the two list columns even.
        policy = self.ui.duplicateLabel.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.ui.duplicateLabel.setSizePolicy(policy)
        self.ui.duplicateLabel.hide()

        self.ui.modelListView.setModel(self.item_model)
        self.ui.modelListView.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.modelListView.customContextMenuRequested.connect(self.show_context_menu)

        self.ui.openAnalysisBtn.clicked.connect(self.start_analysis)

        self.model_dict: Dict[
            str, Optional[Union[DigestOnnxModel, DigestReportModel]]
        ] = {}

        self.analysis_thread: Optional[AnalysisThread] = None
        self.progress: Optional[ProgressDialog] = None
        self.analysis_window = QMainWindow()

        self.current_dir: str = ""
        self.scan_thread = None
        self.scan_progress = None

    def open_progress(self, message: str, num_steps: int):
        self.progress = ProgressDialog(message, num_steps, self)
        self.progress.canceled.connect(self.cancel_analysis)

    def cancel_analysis(self):
        if self.analysis_thread:
            self.analysis_thread.stop_processing()

    def step_progress(self):
        if self.progress:
            self.progress.step()

    def close_progress(self):
        if self.progress:
            self.progress.close()

    def update_message_label(self, info_message: Optional[str] = None) -> None:
        message = f"ℹ️ {info_message}"
        self.ui.infoLabel.setText(message)

    def update_warning_label(self, message: Optional[str] = None) -> None:
        self.ui.warningLabel.setText(f"⚠️ {message}")
        self.ui.warningLabel.show()

    def openFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")

        if folder:  # Only if user selects a file and clicks OK
            self.ui.openAnalysisBtn.setEnabled(True)
            self.set_directory(folder)

    def show_context_menu(self, pos):
        # Get the item that was right-clicked
        index = self.ui.modelListView.indexAt(pos)
        if not index.isValid():
            return

        item = self.item_model.itemFromIndex(index)
        filepath = item.text()  # Get the file path from the item

        # Create context menu
        menu = QMenu()
        open_action = QAction("Open Summary", self)
        open_action.triggered.connect(lambda: (self.model_signal.emit(filepath)))
        menu.addAction(open_action)

        # Show menu at the position of the mouse click
        menu.exec(self.ui.modelListView.viewport().mapToGlobal(pos))

    def update_num_selected_label(self):
        self.model_dict.clear()
        for row in range(self.item_model.rowCount()):
            item = self.item_model.item(row)
            if item.checkState() == Qt.CheckState.Checked:
                self.model_dict[item.data(Qt.ItemDataRole.DisplayRole)] = None

        self.ui.numSelectedLabel.setText(f"{len(self.model_dict)} selected models")
        if self.model_dict:
            self.ui.openAnalysisBtn.setEnabled(True)
        else:
            self.ui.openAnalysisBtn.setEnabled(False)

    def update_list_view_items(self):
        radio_all_state = self.ui.radioAll.isChecked()
        radio_onnx_state = self.ui.radioONNX.isChecked()
        radio_reports_state = self.ui.radioReports.isChecked()
        for row in range(self.item_model.rowCount()):
            item = self.item_model.item(row)
            value = item.data(Qt.ItemDataRole.DisplayRole)
            if radio_all_state:
                item.setCheckState(Qt.CheckState.Checked)
            elif os.path.splitext(value)[-1] == ".onnx" and radio_onnx_state:
                item.setCheckState(Qt.CheckState.Checked)
            elif os.path.splitext(value)[-1] == ".yaml" and radio_reports_state:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

    def set_directory(self, directory: str):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist.")
        if self.scan_thread is not None and self.scan_thread.isRunning():
            return
        self.current_dir = directory
        self.ui.selectFolderBtn.setEnabled(False)
        self.ui.openAnalysisBtn.setEnabled(False)
        self.ui.warningLabel.hide()
        self.item_model.clear()
        self.model_dict.clear()
        self.ui.duplicateListWidget.clear()
        self.ui.duplicateLabel.hide()
        self.update_num_selected_label()
        self.scan_progress = ProgressDialog("Scanning folder...", parent=self)
        self.scan_progress.setRange(0, 0)
        self.scan_thread = FolderScanThread(directory, self)
        self.scan_progress.canceled.connect(self.scan_thread.requestInterruption)
        self.scan_thread.progress.connect(self.scan_progress.setLabelText)
        self.scan_thread.completed.connect(self.show_scan_results)
        self.scan_thread.failed.connect(self.scan_failed)
        self.scan_thread.canceled.connect(self.scan_canceled)
        self.scan_thread.finished.connect(self.finish_scan)
        self.scan_thread.start()

    def show_scan_results(self, result):
        num_duplicates = 0
        self.item_model.blockSignals(True)
        try:
            for paths in result["groups"]:
                if len(paths) > 1:
                    num_duplicates += len(paths) - 1
                    self.ui.duplicateListWidget.addItem(paths[0])
                    for duplicate in paths[1:]:
                        self.ui.duplicateListWidget.addItem(f"- Duplicate: {duplicate}")
                item = QStandardItem(paths[0])
                item.setCheckable(True)
                item.setCheckState(Qt.CheckState.Checked)
                self.item_model.appendRow(item)
            self.update_list_view_items()
        finally:
            self.item_model.blockSignals(False)
        self.update_num_selected_label()
        if num_duplicates:
            self.ui.duplicateLabel.setText(f"Ignoring {num_duplicates} duplicate model(s).")
            self.ui.duplicateLabel.show()
        warnings = []
        if result["limited"]:
            warnings.append("Scan stopped because system memory usage reached 90%.")
        if result["errors"]:
            warnings.append(f"Skipped {result['errors']} unreadable file(s) or folder(s). See the diagnostic log.")
        if warnings:
            self.update_warning_label(" ".join(warnings))
        self.update_message_label(
            f"Found {len(result['groups'])} unique models in {result['total']} candidate files. "
            "Right click a model to open its summary."
        )

    def scan_failed(self, message):
        self.update_warning_label(f"Could not scan this folder: {message}")

    def scan_canceled(self):
        self.update_message_label("Folder scan canceled. Select a folder to try again.")

    def finish_scan(self):
        if self.scan_progress:
            self.scan_progress.close()
            self.scan_progress.deleteLater()
            self.scan_progress = None
        self.ui.selectFolderBtn.setEnabled(True)
        self.update_num_selected_label()
        if self.scan_thread:
            self.scan_thread.deleteLater()
            self.scan_thread = None

    def stop_workers(self):
        if self.scan_thread:
            self.scan_thread.requestInterruption()
            self.scan_thread.wait()
        if self.analysis_thread:
            self.analysis_thread.stop_processing()
            self.analysis_thread.wait()

    def start_analysis(self):

        if not self.model_dict:
            WarnDialog("There are no models to process", self)
            return

        self.analysis_thread = AnalysisThread()
        self.analysis_thread.completed.connect(self.open_analysis)
        self.analysis_thread.close_progress.connect(self.close_progress)
        self.analysis_thread.step_progress.connect(self.step_progress)
        self.analysis_thread.open_progress.connect(self.open_progress)
        self.analysis_thread.model_dict = self.model_dict
        self.analysis_thread.start()

    def open_analysis(
        self, model_list: List[Union[DigestOnnxModel, DigestReportModel]]
    ):
        if not model_list:
            return

        multi_model_analysis = MultiModelAnalysis(model_list)
        self.analysis_window.setCentralWidget(multi_model_analysis)
        self.analysis_window.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))
        self.analysis_window.setWindowTitle("Multi-Model Analysis")
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.analysis_window.resize(
            int(screen_geometry.width() / 1.5), int(screen_geometry.height() * 0.80)
        )
        self.analysis_window.show()
