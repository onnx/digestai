# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
# pylint: disable=wrong-import-position

import os
import sys
import shutil
import argparse
from typing import Dict, Tuple, Optional
import tempfile
from enum import IntEnum
import pandas as pd
import yaml

# This is a temporary workaround since the Qt designer generated files
# do not import from the gui package.
ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, str(ROOT_FOLDER))

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QPushButton,
    QMainWindow,
    QLabel,
    QTextEdit,
    QHBoxLayout,
    QWidget,
    QFrame,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QMenu,
)
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QIcon, QFont
from PySide6.QtCore import Qt, QSize, QThreadPool

from digest.dialog import StatusDialog, InfoDialog, WarnDialog, ProgressDialog
from digest.similarity_analysis import SimilarityWorker, post_process
from digest.popup_window import PopupWindow
from digest.huggingface_page import HuggingfacePage
from digest.multi_model_selection_page import MultiModelSelectionPage
from digest.ui.mainwindow_ui import Ui_MainWindow
from digest.modelsummary import modelSummary
from digest.node_summary import NodeSummary
from digest.qt_utils import apply_dark_style_sheet
from digest.model_class.digest_model import SupportedModelTypes, DigestModel
from digest.model_class.digest_onnx_model import (
    DigestOnnxModel,
    LoadDigestOnnxModelWorker,
)
from digest.model_class.digest_report_model import (
    DigestReportModel,
    LoadDigestReportModelWorker,
)
from utils import onnx_utils


class DigestConfig:
    GUI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "gui_config.yaml")
    SUPPORTED_EXTENSIONS = [".onnx", ".yaml"]


class SimilarityAnalysisReport(QMainWindow):
    def __init__(self, image_path, most_similar_models):
        super().__init__()

        self.setWindowTitle("Similarity Analysis Report")
        self.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a layout
        layout = QHBoxLayout(main_widget)

        # Create QLabel to display the enlarged image
        self.enlarged_image_label = QLabel()
        layout.addWidget(self.enlarged_image_label)

        # Set the image
        self.image_path = image_path
        self.update_enlarged_image()

        # Create a frame for the text
        text_frame = QFrame()
        text_frame.setMinimumWidth(500)
        text_frame.setMaximumWidth(550)
        text_layout = QVBoxLayout(text_frame)
        text_layout.setContentsMargins(20, 100, 100, 20)

        # Title
        self.title_label = QLabel("Similarity Analysis Heatmap")
        title_font = QFont("DejaVu Sans", 20)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)
        text_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Text description
        self.description_textedit = QTextEdit()
        self.description_textedit.setReadOnly(True)
        self.description_textedit.setMinimumHeight(600)
        self.description_textedit.setHtml(
            f"""
            <p style="font-family: 'DejaVu Sans'; font-size: 12pt; color: white; 
            text-align: justify;"><br>This analysis works by extracting ops and subgraphs from the 
            target model and comparing it with all models in a database. Our database contains over 
            1,900 LLMs, transformers, and computer vision (TIMM) models. <br><br>
            Operators and subgraphs shown in Yellow <span style="color: yellow; font-size: 20px">
            &#9632;</span> represent elements that strongly correlate with the target model, while 
            operators and subgraphs shown in Purple <span style="color: purple; font-size: 20px;">
            &#9632;</span> represent elements that are weakly correlated.<br>
            <h2>The most similar models found were:</h2>
            <ul style="font-family: 'Courier New', Courier, monospace;">
                <li>{most_similar_models[0]}</li>
                <li>{most_similar_models[1]}</li>
                <li>{most_similar_models[2]}</li>
            </ul>
            </p>
            """
        )
        text_layout.addWidget(self.description_textedit)

        # Add text frame to layout
        layout.addWidget(text_frame)

        # Spacer
        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        text_layout.addItem(spacer)

        # Connect resize event to update image size
        self.resizeEvent = lambda event: self.update_enlarged_image()

    def update_enlarged_image(self):
        pixmap = QPixmap(self.image_path)
        max_image_width = int(self.width() * 0.6)
        pixmap = pixmap.scaledToWidth(
            max_image_width, Qt.TransformationMode.SmoothTransformation
        )
        self.enlarged_image_label.setPixmap(pixmap)

    def contextMenuEvent(self, event):
        menu = QMenu()
        copy_action = menu.addAction("Copy Image")
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == copy_action:
            self.copy_chart_to_clipboard()

    def copy_chart_to_clipboard(self):
        pixmap = QPixmap(self.enlarged_image_label.grab())
        QApplication.clipboard().setPixmap(pixmap)


class ModelLoadError(Exception):
    """Raised when there's an error loading a model."""


class DigestApp(QMainWindow):

    class Page(IntEnum):
        SPLASH = 0
        SUMMARY = 1
        HUGGINGFACE = 2
        SUBGRAPH = 3
        MULTIMODEL = 4

    def __init__(self, model_file: Optional[str] = None):
        super(DigestApp, self).__init__()
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread_pool: QThreadPool = QThreadPool()

        self.nodes_window: Dict[str, PopupWindow] = {}
        self.status_dialog: Optional[StatusDialog] = None
        self.err_open_dialog: Optional[StatusDialog] = None
        self.temp_dir: tempfile.TemporaryDirectory = tempfile.TemporaryDirectory()
        self.digest_models: Dict[str, DigestModel] = {}

        self.model_similarity_report: Dict[str, SimilarityAnalysisReport] = {}

        self.ui.singleModelWidget.hide()
        self.ui.subgraphBtn.hide()

        self.ui.stackedWidget.setCurrentIndex(self.Page.SPLASH)
        self.ui.stackedWidget.dragEnterEvent = self.dragEnterEvent
        self.ui.stackedWidget.dropEvent = self.dropEvent

        # By default keep it disabled until all threads are done
        self.ui.saveBtn.setEnabled(False)

        self.ui.logoBtn.clicked.connect(self.logo_clicked)
        self.ui.openFileBtn.clicked.connect(self.openFile)
        self.ui.openFolderBtn.clicked.connect(self.multi_model_clicked)
        self.ui.huggingfaceBtn.clicked.connect(self.huggingface_clicked)
        self.ui.summaryBtn.clicked.connect(self.summary_clicked)
        self.ui.saveBtn.clicked.connect(self.save_reports)
        self.ui.nodesListBtn.clicked.connect(self.open_node_summary)
        self.ui.subgraphBtn.clicked.connect(self.subgraph_toggled)
        self.ui.infoBtn.clicked.connect(self.show_info_dialog)
        self.infoDialog = None

        self.load_progress: Optional[ProgressDialog] = None

        enable_huggingface_model = True
        with open(DigestConfig.GUI_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            enable_huggingface_model = config["modules"]["huggingface"]

        if not enable_huggingface_model:
            self.ui.huggingfaceBtn.hide()

        self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.ui.tabWidget.currentChanged.connect(self.tab_focused)
        self.current_tab_index = 0
        self.ui.tabWidget.removeTab(0)

        # These two flags are used to keep the save button disabled until the
        # similarity and stats threads are compelete.
        self.similarity_save_button_flag: Dict[str, bool] = {}
        self.stats_save_button_flag: Dict[str, bool] = {}

        # Set up the HUGGINGFACE Page
        huggingface_page = HuggingfacePage()
        huggingface_page.model_signal.connect(self.load_model)
        self.ui.stackedWidget.insertWidget(self.Page.HUGGINGFACE, huggingface_page)

        # Set up the multi model page and relevant button
        self.multimodelselection_page = MultiModelSelectionPage()
        self.ui.stackedWidget.insertWidget(
            self.Page.MULTIMODEL, self.multimodelselection_page
        )
        self.multimodelselection_page.model_signal.connect(self.load_model)

        # Load model file if given as input to the executable
        if model_file:
            self.load_model(model_file)

    def uncheck_single_model_buttons(self):
        for button in self.ui.singleModelWidget.findChildren(QPushButton):
            button.setChecked(False)

    def uncheck_ingest_buttons(self):
        for button in self.ui.ingestWidget.findChildren(QPushButton):
            button.setChecked(False)

    def tab_focused(self, index):
        widget = self.ui.tabWidget.widget(index)
        if isinstance(widget, modelSummary):
            model_id = widget.model_id
            if (
                self.stats_save_button_flag[model_id]
                and self.similarity_save_button_flag[model_id]
                and not widget.model_type == SupportedModelTypes.REPORT
            ):
                self.ui.saveBtn.setEnabled(True)
            else:
                self.ui.saveBtn.setEnabled(False)

    def closeTab(self, index):
        summary_widget = self.ui.tabWidget.widget(index)
        if isinstance(summary_widget, modelSummary):
            model_id = summary_widget.model_id
            summary_widget.deleteLater()

            # delete the digest model to free up used memory
            if model_id in self.digest_models:
                del self.digest_models[model_id]

        self.ui.tabWidget.removeTab(index)
        if self.ui.tabWidget.count() == 0:
            self.ui.stackedWidget.setCurrentIndex(self.Page.SPLASH)
            self.ui.singleModelWidget.hide()

    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "ONNX and Report Files (*.onnx  *.yaml)"
        )

        if not file_name:
            return

        self.load_model(file_name)

    def open_similarity_report(self, model_id: str, image_path, most_similar_models):
        self.model_similarity_report[model_id] = SimilarityAnalysisReport(
            image_path, most_similar_models
        )
        self.model_similarity_report[model_id].show()

    def update_similarity_widget(
        self,
        completed_successfully: bool,
        model_id: str,
        most_similar: str,
        png_filepath: Optional[str] = None,
        df_sorted: Optional[pd.DataFrame] = None,
    ):
        widget = None
        curr_index = -1
        for index in range(self.ui.tabWidget.count()):
            tab_widget = self.ui.tabWidget.widget(index)
            if isinstance(tab_widget, modelSummary) and tab_widget.model_id == model_id:
                widget = tab_widget
                curr_index = index
                break

        # convert back to a List[str]
        most_similar_list = most_similar.split(",")

        if completed_successfully and isinstance(widget, modelSummary) and png_filepath:

            if df_sorted is not None:
                post_process(
                    self.digest_models[model_id].model_name,
                    most_similar_list,
                    df_sorted,
                    png_filepath,
                )

            widget.load_gif.stop()
            widget.ui.similarityImg.clear()
            # We give the image a 10% haircut to fit it more aesthetically
            widget_width = widget.ui.similarityImg.width()

            pixmap = QPixmap(png_filepath)
            aspect_ratio = pixmap.width() / pixmap.height()
            target_height = int(widget_width / aspect_ratio)
            pixmap_scaled = pixmap.scaled(
                QSize(widget_width, target_height),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            widget.ui.similarityImg.setPixmap(pixmap_scaled)
            widget.ui.similarityImg.setText("")
            widget.ui.similarityImg.setCursor(Qt.CursorShape.PointingHandCursor)

            # Show most correlated models
            widget.ui.similarityCorrelation.show()
            widget.ui.similarityCorrelationStatic.show()

            most_similar_list = most_similar_list[1:4]
            if most_similar:
                text = (
                    "\n<span style='color:red;text-align:center;'>"
                    f"{most_similar_list[0]}, {most_similar_list[1]}, "
                    f"and {most_similar_list[2]}. "
                    "</span>"
                )
            else:
                # currently the similarity widget expects the most_similar_models
                # to allows contains 3 models. For now we will just send three empty
                # strings but at some point we should handle an arbitrary case.
                most_similar_list = ["", "", ""]
                text = "NTD"

            # Create option to click to enlarge image
            widget.ui.similarityImg.mousePressEvent = (
                lambda event: self.open_similarity_report(
                    model_id, png_filepath, most_similar_list
                )
            )
            # Create option to click to enlarge image
            self.model_similarity_report[model_id] = SimilarityAnalysisReport(
                png_filepath, most_similar_list
            )

            widget.ui.similarityCorrelation.setText(text)
        elif isinstance(widget, modelSummary):
            # Remove animation and set text to failing message
            widget.load_gif.stop()
            widget.ui.similarityImg.clear()
            widget.ui.similarityImg.setText("Failed to perform similarity analysis")
        else:
            print(
                f"Tab widget is of type {type(widget)} and not of type modelSummary "
                "which is unexpected."
            )

        self.similarity_save_button_flag[model_id] = True
        if self.ui.tabWidget.currentIndex() == curr_index:
            if self.stats_save_button_flag[model_id] and not isinstance(
                self.digest_models[model_id], DigestReportModel
            ):
                self.ui.saveBtn.setEnabled(True)

    def load_model(self, file_path: str) -> None:
        try:
            file_path = os.path.normpath(file_path)
            if not os.path.exists(file_path):
                raise ModelLoadError(f"Model file {file_path} does not exist.")

            basename, file_ext = os.path.splitext(os.path.basename(file_path))
            supported_exts = [".onnx", ".yaml"]

            if file_ext not in supported_exts:
                raise ModelLoadError(
                    f"Digest does not support files with the extension {file_ext}"
                )

            # Before opening the file, check to see if it is already opened.
            for index in range(self.ui.tabWidget.count()):
                widget = self.ui.tabWidget.widget(index)
                if isinstance(widget, modelSummary) and file_path == widget.file:
                    self.ui.tabWidget.setCurrentIndex(index)
                    return

            self.load_progress = ProgressDialog("Loading Model...", 3, self)
            self.load_progress.step()

            self.load_progress.setLabelText(
                "Creating a Digest model. "
                "Please be patient as this could take a minute."
            )

            # Initialize worker variable
            digest_model_worker = None

            if file_ext == ".onnx":
                digest_model_worker = LoadDigestOnnxModelWorker(
                    model_name=basename, model_file_path=file_path
                )
            elif file_ext == ".yaml":
                digest_model_worker = LoadDigestReportModelWorker(
                    model_name=basename, model_file_path=file_path
                )

            if digest_model_worker is not None:
                digest_model_worker.signals.completed.connect(self.post_load_model)
                self.thread_pool.start(digest_model_worker)
        except ModelLoadError as e:
            self.status_dialog = StatusDialog(str(e), parent=self)
            self.status_dialog.show()
        except Exception as e:  # pylint: disable=broad-except
            self.status_dialog = StatusDialog(
                f"Unexpected error loading model: {str(e)}", parent=self
            )
            self.status_dialog.show()

    def post_load_model(self, digest_model: DigestModel):
        """This function is automatically run after the model load workers are finished"""

        if self.load_progress:
            self.load_progress.step()
            self.load_progress.setLabelText("Displaying the model summary")

        if digest_model.unique_id:
            model_id = digest_model.unique_id
        else:

            if self.load_progress:
                self.load_progress.close()

            self.status_dialog = StatusDialog(
                "Unexpected Error: Digest model did not return a valid ID.",
                parent=self,
            )
            self.status_dialog.show()
            print("Unexpected Error: Digest model did not return a valid ID.")
            return

        self.stats_save_button_flag[model_id] = False
        self.similarity_save_button_flag[model_id] = False

        # Every time an onnx is loaded we should emulate a model summary button click
        self.summary_clicked()
        self.digest_models[model_id] = digest_model

        model_summary = modelSummary(self.digest_models[model_id])
        if model_summary.freeze_inputs:
            model_summary.freeze_inputs.complete_signal.connect(self.load_model)

        self.ui.tabWidget.addTab(model_summary, "")

        new_tab_idx = self.ui.tabWidget.count() - 1
        self.ui.tabWidget.setTabText(new_tab_idx, "".join(digest_model.model_name))
        self.ui.tabWidget.setCurrentIndex(new_tab_idx)
        self.ui.stackedWidget.setCurrentIndex(self.Page.SUMMARY)
        self.ui.singleModelWidget.show()

        if self.load_progress:
            self.load_progress.step()

        if isinstance(digest_model, DigestOnnxModel) and digest_model.model_proto:
            self.stats_save_button_flag[model_id] = True
            dynamic_input_dims = onnx_utils.get_dynamic_input_dims(
                digest_model.model_proto
            )
            if dynamic_input_dims:
                model_summary.ui.freezeButton.setVisible(True)
                model_summary.ui.warningLabel.setText(
                    "⚠️ Some model details are unavailable due to dynamic input dimensions. "
                    "See section Input Tensor(s) Information below for more details."
                )
                model_summary.ui.warningLabel.show()

            # Start similarity Analysis
            # Note: Should only be started after the model tab has been created
            png_tmp_path = os.path.join(self.temp_dir.name, model_id)
            os.makedirs(png_tmp_path, exist_ok=True)
            assert os.path.exists(png_tmp_path), f"Error with creating {png_tmp_path}"
            png_file_path = os.path.join(
                png_tmp_path, f"heatmap_{digest_model.model_name}.png"
            )

            model_summary.png_file_path = png_file_path

            similarity_worker = SimilarityWorker(
                digest_model.filepath, png_file_path, model_id
            )
            similarity_worker.signals.completed.connect(self.update_similarity_widget)
            self.thread_pool.start(similarity_worker)

        elif isinstance(digest_model, DigestReportModel):
            self.update_similarity_widget(
                bool(digest_model.similarity_heatmap_path),
                model_id=model_id,
                most_similar="",
                png_filepath=digest_model.similarity_heatmap_path,
            )

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.load_model(file_path)

    ## functions for changing menu page
    def logo_clicked(self):
        self.uncheck_single_model_buttons()
        self.uncheck_ingest_buttons()
        self.ui.stackedWidget.setCurrentIndex(self.Page.SPLASH)

    def summary_clicked(self):
        self.uncheck_single_model_buttons()
        self.uncheck_ingest_buttons()
        self.ui.summaryBtn.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(self.Page.SUMMARY)

    def subgraph_toggled(self):
        self.uncheck_single_model_buttons()
        self.uncheck_ingest_buttons()
        self.ui.subgraphBtn.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(self.Page.SUBGRAPH)

    def multi_model_clicked(self):
        self.uncheck_single_model_buttons()
        self.uncheck_ingest_buttons()
        self.ui.openFolderBtn.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(self.Page.MULTIMODEL)

    def huggingface_clicked(self):
        self.uncheck_single_model_buttons()
        self.uncheck_ingest_buttons()
        self.ui.huggingfaceBtn.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(self.Page.HUGGINGFACE)

    def save_reports(self):
        """Saves the contents of a model summary"""
        current_tab = self.ui.tabWidget.currentWidget()
        if not isinstance(current_tab, modelSummary):
            return

        save_directory = self._get_save_directory()
        if not save_directory:
            return

        try:
            self._save_report_files(current_tab, save_directory)
        except Exception as exception:  # pylint: disable=broad-except
            self._handle_save_error(exception)
        else:
            self._show_save_success(save_directory)

    def _get_save_directory(self) -> Optional[str]:
        """Get and validate the save directory from user."""
        directory = QFileDialog(self).getExistingDirectory(self, "Select Directory")
        if not directory:
            return None

        if not os.path.exists(directory) or not os.access(directory, os.W_OK):
            self.show_warning_dialog(
                f"The directory {directory} is not valid or writable."
            )
            return None

        return directory

    def _save_report_files(self, current_tab, save_directory):
        model_name = current_tab.ui.modelName.text()

        # Save the node histogram image
        node_histogram = current_tab.ui.opHistogramChart.grab()
        node_histogram.save(
            os.path.join(save_directory, f"{model_name}_histogram.png"), "PNG"
        )

        # Save csv of node type counts
        node_type_filepath = os.path.join(
            save_directory, f"{model_name}_node_type_counts.csv"
        )

        self.digest_models[current_tab.model_id].save_node_type_counts_csv_report(
            node_type_filepath
        )

        # Save (copy) the similarity image
        png_file_path = current_tab.png_file_path

        png_save_path = os.path.join(save_directory, f"{model_name}_heatmap.png")
        if png_file_path and os.path.exists(png_file_path):
            shutil.copy(png_file_path, png_save_path)

        # Save the text report
        txt_report_filepath = os.path.join(save_directory, f"{model_name}_report.txt")
        self.digest_models[current_tab.model_id].save_text_report(txt_report_filepath)

        # Save the yaml report
        yaml_report_filepath = os.path.join(save_directory, f"{model_name}_report.yaml")
        self.digest_models[current_tab.model_id].save_yaml_report(yaml_report_filepath)

        # Save the node list
        nodes_report_filepath = os.path.join(save_directory, f"{model_name}_nodes.csv")

        self.save_nodes_csv(nodes_report_filepath, False)

    def _handle_save_error(self, exception):
        self.status_dialog = StatusDialog(f"{exception}")
        self.status_dialog.show()

    def _show_save_success(self, save_directory):
        self.status_dialog = StatusDialog(
            f"Saved reports to: \n{os.path.abspath(save_directory)}",
            "Successfully saved reports!",
        )
        self.status_dialog.show()

    def on_dialog_closed(self):
        self.infoDialog = None

    def show_info_dialog(self):
        if self.infoDialog is None:
            self.infoDialog = InfoDialog(self)
            self.infoDialog.finished.connect(
                self.on_dialog_closed
            )  # Connect to finished signal
            self.infoDialog.show()
        else:
            self.infoDialog.close()

    def show_warning_dialog(self, warning_message: str):
        warning_dialog = WarnDialog(warning_message, parent=self)
        warning_dialog.show()

    def save_file_dialog(
        self, prompt: str = "Save CSV", file_type: str = "CSV(*.csv)"
    ) -> Tuple[str, str]:
        """Convenience function to open a save file as dialog.
        The getSaveFileName function returns the path and the selected filter.
        """
        path, filter_type = QFileDialog.getSaveFileName(
            self, prompt, os.getcwd(), file_type
        )
        return path, filter_type

    def save_parameters_csv(self, filepath: str, open_dialog: bool = True):
        self.save_nodes_csv(filepath, open_dialog)

    def save_flops_csv(self, filepath: str, open_dialog: bool = True):
        self.save_nodes_csv(filepath, open_dialog)

    def save_nodes_csv(self, csv_filepath: Optional[str], open_dialog: bool = True):
        if open_dialog:
            csv_filepath, _ = self.save_file_dialog()
        if not csv_filepath:
            raise ValueError("A filepath must be given.")
        current_tab = self.ui.tabWidget.currentWidget()
        if isinstance(current_tab, modelSummary):
            self.digest_models[current_tab.model_id].save_nodes_csv_report(csv_filepath)

    def save_chart(self, chart_view):
        path, _ = self.save_file_dialog("Save PNG", "PNG(*.png)")

        # Capture the current view of the chart_view widget
        pixmap = chart_view.grab()

        # Save the pixmap as a PNG image
        pixmap.save(path, "PNG")

    def open_node_summary(self):
        current_tab = self.ui.tabWidget.currentWidget()
        if not isinstance(current_tab, modelSummary):
            return

        model_name = current_tab.ui.modelName.text()
        model_id = current_tab.model_id
        if model_id in self.nodes_window:
            del self.nodes_window[model_id]

        digest_models = self.digest_models[model_id]

        node_summary = NodeSummary(
            model_name=model_name, node_data=digest_models.node_data
        )

        self.nodes_window[model_id] = PopupWindow(
            node_summary, f"{model_name} Nodes Summary"
        )
        self.nodes_window[model_id].destroyed.connect(
            lambda: self.nodes_window.pop(model_id, None)
        )
        self.nodes_window[model_id].open()

    def closeEvent(self, event):
        """Ensure proper cleanup of resources when closing the application."""
        try:
            # Close all child windows
            for window in QApplication.topLevelWidgets():
                if window != self:
                    window.close()

            # Cleanup temporary directory
            if hasattr(self, "temp_dir"):
                self.temp_dir.cleanup()

            # Wait for thread pool to finish
            if hasattr(self, "thread_pool"):
                self.thread_pool.waitForDone()

        finally:
            super().closeEvent(event)


def main():

    parser = argparse.ArgumentParser(
        description="",
    )
    parser.add_argument(
        "-i",
        "--input-file",
        type=str,
        required=False,
        help="Provide the path to a model file.",
    )

    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    apply_dark_style_sheet(app)

    window = DigestApp(args.input_file)
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
