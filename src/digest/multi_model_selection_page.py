# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import glob
from typing import List, Optional, Dict, Union
from collections import defaultdict
from google.protobuf.message import DecodeError
import onnx

# pylint: disable=no-name-in-module
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
from digest.qt_utils import apply_dark_style_sheet, prompt_user_ram_limit
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.model_class.digest_report_model import DigestReportModel, compare_yaml_files
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
                break
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

        model_list = [model for model in self.model_dict.values()]

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
        """
        Recursively searches a directory for onnx models and yaml report files.
        """

        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist.")

        if directory != self.current_dir:
            self.current_dir = directory
        else:
            return

        progress = ProgressDialog("Searching directory for model files", 0, self)

        onnx_file_list = list(
            glob.glob(os.path.join(directory, "**/*.onnx"), recursive=True)
        )
        onnx_file_list = [os.path.normpath(model_file) for model_file in onnx_file_list]

        yaml_file_list = list(
            glob.glob(os.path.join(directory, "**/*.yaml"), recursive=True)
        )
        yaml_file_list = [os.path.normpath(model_file) for model_file in yaml_file_list]

        # Filter out YAML files that are not valid reports
        report_file_list = []
        for yaml_file in yaml_file_list:
            digest_report = DigestReportModel(yaml_file)
            if digest_report.is_valid:
                report_file_list.append(yaml_file)

        total_num_models = len(onnx_file_list) + len(report_file_list)

        serialized_models_paths: defaultdict[bytes, List[str]] = defaultdict(list)

        progress.close()
        progress = ProgressDialog("Loading models", total_num_models, self)

        memory_limit_percentage = 90
        models_loaded = 0
        for filepath in onnx_file_list + report_file_list:
            progress.step()
            if progress.user_canceled:
                break
            try:
                models_loaded += 1
                extension = os.path.splitext(filepath)[-1]
                if extension == ".onnx":
                    model = onnx.load(filepath, load_external_data=False)
                    serialized_models_paths[model.SerializeToString()].append(filepath)
                elif extension == ".yaml":
                    pass
                dialog_msg = (
                    "Warning: System RAM has exceeded the threshold of "
                    f"{memory_limit_percentage}%. No further models will be loaded. "
                )
                if prompt_user_ram_limit(
                    sys_ram_percent_limit=memory_limit_percentage,
                    message=dialog_msg,
                    parent=self,
                ):
                    self.update_warning_label(
                        f"Loaded only {models_loaded - 1} out of {total_num_models} models "
                        f"as memory consumption has reached {memory_limit_percentage}% of "
                        "system memory. Preventing further loading of models."
                    )
                    print(
                        "Preventing further model loads as mem consumption exceeded "
                        f"{memory_limit_percentage}%"
                    )
                    break
                else:
                    self.ui.warningLabel.hide()

            except DecodeError as error:
                print(f"Error decoding model {filepath}: {error}")

        progress.close()

        progress = ProgressDialog("Processing Models", total_num_models, self)

        num_duplicates = 0
        self.item_model.clear()
        self.ui.duplicateListWidget.clear()
        for paths in serialized_models_paths.values():
            progress.step()
            if progress.user_canceled:
                break
            if len(paths) > 1:
                num_duplicates += 1
                self.ui.duplicateListWidget.addItem(paths[0])
                for dupe in paths[1:]:
                    self.ui.duplicateListWidget.addItem(f"- Duplicate: {dupe}")
            item = QStandardItem(paths[0])
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Checked)
            self.item_model.appendRow(item)

        # Use a standard nested loop to detect duplicate reports
        duplicate_reports: Dict[str, List[str]] = {}
        processed_files = set()
        for i in range(len(report_file_list)):
            progress.step()
            if progress.user_canceled:
                break
            path1 = report_file_list[i]
            if path1 in processed_files:
                continue  # Skip already processed files

            # We will use path1 as the unique model and save a list of duplicates
            duplicate_reports[path1] = []
            for j in range(i + 1, len(report_file_list)):
                path2 = report_file_list[j]
                if compare_yaml_files(
                    path1, path2, ["report_date", "model_files", "digest_version"]
                ):
                    num_duplicates += 1
                    duplicate_reports[path1].append(path2)
                    processed_files.add(path2)

        for path, dupes in duplicate_reports.items():
            if dupes:
                self.ui.duplicateListWidget.addItem(path)
                for dupe in dupes:
                    self.ui.duplicateListWidget.addItem(f"- Duplicate: {dupe}")
            item = QStandardItem(path)
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Checked)
            self.item_model.appendRow(item)

        progress.close()

        if num_duplicates:
            label_text = f"Ignoring {num_duplicates} duplicate model(s)."
            self.ui.duplicateLabel.setText(label_text)
            self.ui.duplicateLabel.show()
        else:
            self.ui.duplicateLabel.hide()

        self.update_num_selected_label()

        self.update_message_label(
            f"Found a total of {total_num_models} model files. "
            "Right click a model below "
            "to open it up in the model summary view."
        )

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
