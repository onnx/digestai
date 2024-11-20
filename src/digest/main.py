# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
# pylint: disable=wrong-import-position

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, Tuple, Optional
import tempfile
from enum import IntEnum
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
    QTableWidgetItem,
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
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QMovie, QIcon, QFont
from PySide6.QtCore import Qt, QDir

from digest.dialog import StatusDialog, InfoDialog, WarnDialog, ProgressDialog
from digest.thread import StatsThread, SimilarityThread
from digest.popup_window import PopupWindow
from digest.huggingface_page import HuggingfacePage
from digest.multi_model_selection_page import MultiModelSelectionPage
from digest.ui.mainwindow_ui import Ui_MainWindow
from digest.modelsummary import modelSummary
from digest.node_summary import NodeSummary
from digest.qt_utils import apply_dark_style_sheet
from utils import onnx_utils

GUI_CONFIG = os.path.join(os.path.dirname(__file__), "gui_config.yaml")


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


class DigestApp(QMainWindow):

    class Page(IntEnum):
        SPLASH = 0
        SUMMARY = 1
        HUGGINGFACE = 2
        SUBGRAPH = 3
        MULTIMODEL = 4

    def __init__(self, model_file: Optional[str] = None):
        super(DigestApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.nodes_window: Dict[str, PopupWindow] = {}
        self.status_dialog = None
        self.err_open_dialog = None
        self.temp_dir = tempfile.TemporaryDirectory()
        self.digest_models: Dict[str, onnx_utils.DigestOnnxModel] = {}

        # QThread containers
        self.model_nodes_stats_thread: Dict[str, StatsThread] = {}
        self.model_similarity_thread: Dict[str, SimilarityThread] = {}
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

        enable_huggingface_model = True
        with open(GUI_CONFIG, "r", encoding="utf-8") as f:
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
        huggingface_page.model_signal.connect(self.load_onnx)
        self.ui.stackedWidget.insertWidget(self.Page.HUGGINGFACE, huggingface_page)

        # Set up the multi model page and relevant button
        self.multimodelselection_page = MultiModelSelectionPage()
        self.ui.stackedWidget.insertWidget(
            self.Page.MULTIMODEL, self.multimodelselection_page
        )
        self.multimodelselection_page.model_signal.connect(self.load_onnx)

        # Load model file if given as input to the executable
        if model_file:
            if (
                os.path.exists(model_file)
                and os.path.splitext(model_file)[-1] == ".onnx"
            ):
                self.load_onnx(model_file)
            else:
                self.err_open_dialog = StatusDialog(
                    f"Could not open {model_file}", parent=self
                )
                self.err_open_dialog.show()

    def uncheck_single_model_buttons(self):
        for button in self.ui.singleModelWidget.findChildren(QPushButton):
            button.setChecked(False)

    def uncheck_ingest_buttons(self):
        for button in self.ui.ingestWidget.findChildren(QPushButton):
            button.setChecked(False)

    def tab_focused(self, index):
        widget = self.ui.tabWidget.widget(index)
        if isinstance(widget, modelSummary):
            model_id = widget.digest_model.unique_id
            if (
                self.stats_save_button_flag[model_id]
                and self.similarity_save_button_flag[model_id]
            ):
                self.ui.saveBtn.setEnabled(True)
            else:
                self.ui.saveBtn.setEnabled(False)

    def closeTab(self, index):
        summary_widget = self.ui.tabWidget.widget(index)
        if isinstance(summary_widget, modelSummary):
            unique_id = summary_widget.digest_model.unique_id
            summary_widget.deleteLater()
            tab_thread = self.model_nodes_stats_thread[unique_id]
            if tab_thread:
                tab_thread.exit()
                if not tab_thread.isRunning():
                    del self.model_nodes_stats_thread[unique_id]
            # delete the digest model to free up used memory
            if unique_id in self.digest_models:
                del self.digest_models[unique_id]

        self.ui.tabWidget.removeTab(index)
        if self.ui.tabWidget.count() == 0:
            self.ui.stackedWidget.setCurrentIndex(self.Page.SPLASH)
            self.ui.singleModelWidget.hide()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "ONNX Files (*.onnx)"
        )

        if (
            filename and os.path.splitext(filename)[-1] == ".onnx"
        ):  # Only if user selects a file and clicks OK
            self.load_onnx(filename)

    def update_flops_label(
        self,
        digest_model: onnx_utils.DigestOnnxModel,
        unique_id: str,
    ):
        self.digest_models[unique_id].model_flops = digest_model.model_flops
        self.digest_models[unique_id].node_type_flops = digest_model.node_type_flops
        self.digest_models[unique_id].model_parameters = digest_model.model_parameters
        self.digest_models[unique_id].node_type_parameters = (
            digest_model.node_type_parameters
        )
        self.digest_models[unique_id].per_node_info = digest_model.per_node_info

        # We must iterate over the tabWidget and match to the tab_name because the user
        # may have switched the currentTab during the threads execution.
        for index in range(self.ui.tabWidget.count()):
            widget = self.ui.tabWidget.widget(index)
            if (
                isinstance(widget, modelSummary)
                and widget.digest_model.unique_id == unique_id
            ):
                if digest_model.model_flops is None:
                    flops_str = "--"
                else:
                    flops_str = format(digest_model.model_flops, ",")

                    # Set up the pie chart
                    pie_chart_labels, pie_chart_data = zip(
                        *self.digest_models[unique_id].node_type_flops.items()
                    )
                    widget.ui.flopsPieChart.set_data(
                        "FLOPs Intensity Per Op Type",
                        pie_chart_labels,
                        pie_chart_data,
                    )

                widget.ui.flops.setText(flops_str)

                # Set up the pie chart
                pie_chart_labels, pie_chart_data = zip(
                    *self.digest_models[unique_id].node_type_parameters.items()
                )
                widget.ui.parametersPieChart.set_data(
                    "Parameter Intensity Per Op Type",
                    pie_chart_labels,
                    pie_chart_data,
                )
                break

        self.stats_save_button_flag[unique_id] = True
        if self.ui.tabWidget.currentIndex() == index:
            if self.similarity_save_button_flag[unique_id]:
                self.ui.saveBtn.setEnabled(True)

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
        png_filepath: str,
    ):

        widget = None
        for index in range(self.ui.tabWidget.count()):
            tab_widget = self.ui.tabWidget.widget(index)
            if (
                isinstance(tab_widget, modelSummary)
                and tab_widget.digest_model.unique_id == model_id
            ):
                widget = tab_widget
                break

        if completed_successfully and isinstance(widget, modelSummary):
            widget_width = widget.ui.similarityImg.width()
            widget.ui.similarityImg.setPixmap(
                QPixmap(png_filepath).scaledToWidth(widget_width)
            )
            widget.ui.similarityImg.setText("")
            widget.ui.similarityImg.setCursor(Qt.CursorShape.PointingHandCursor)

            # Show most correlated models
            widget.ui.similarityCorrelation.show()
            widget.ui.similarityCorrelationStatic.show()
            most_similar_models = most_similar.split(",")
            text = (
                "\n<span style='color:red;text-align:center;'>"
                f"{most_similar_models[0]}, {most_similar_models[1]}, and {most_similar_models[2]}."
                "</span>"
            )

            # Create option to click to enlarge image
            widget.ui.similarityImg.mousePressEvent = (
                lambda event: self.open_similarity_report(
                    model_id, png_filepath, most_similar_models
                )
            )
            # Create option to click to enlarge image
            self.model_similarity_report[model_id] = SimilarityAnalysisReport(
                png_filepath, most_similar_models
            )

            widget.ui.similarityCorrelation.setText(text)
        elif isinstance(widget, modelSummary):
            # Remove animation and set text to failing message
            widget.ui.similarityImg.setMovie(QMovie(None))
            widget.ui.similarityImg.setText("Failed to perform similarity analysis")
        else:
            print("Tab widget is not of type modelSummary which is unexpected.")

        #
        self.similarity_save_button_flag[model_id] = True
        if self.ui.tabWidget.currentIndex() == index:
            if self.stats_save_button_flag[model_id]:
                self.ui.saveBtn.setEnabled(True)

    def load_onnx(self, filepath: str):

        # Ensure the filepath follows a standard formatting:
        filepath = os.path.normpath(filepath)

        if not os.path.exists(filepath):
            return

        # Every time an onnx is loaded we should emulate a model summary button click
        self.summary_clicked()

        # Before opening the file, check to see if it is already opened.
        for index in range(self.ui.tabWidget.count()):
            widget = self.ui.tabWidget.widget(index)
            if isinstance(widget, modelSummary) and filepath == widget.file:
                self.ui.tabWidget.setCurrentIndex(index)
                return

        try:

            progress = ProgressDialog("Loading & Optimizing ONNX Model...", 8, self)
            QApplication.processEvents()  # Process pending events

            model = onnx_utils.load_onnx(filepath, load_external_data=False)
            opt_model, opt_passed = onnx_utils.optimize_onnx_model(model)
            progress.step()

            basename = os.path.splitext(os.path.basename(filepath))
            model_name = basename[0]

            digest_model = onnx_utils.DigestOnnxModel(
                onnx_model=model, model_name=model_name, save_proto=False
            )
            model_id = digest_model.unique_id

            self.stats_save_button_flag[model_id] = False
            self.similarity_save_button_flag[model_id] = False

            self.digest_models[model_id] = digest_model

            # We must set the proto for the model_summary freeze_inputs
            self.digest_models[model_id].model_proto = opt_model

            model_summary = modelSummary(self.digest_models[model_id])
            model_summary.freeze_inputs.complete_signal.connect(self.load_onnx)

            dynamic_input_dims = onnx_utils.get_dynamic_input_dims(opt_model)
            if dynamic_input_dims:
                model_summary.ui.freezeButton.setVisible(True)
                model_summary.ui.warningLabel.setText(
                    "⚠️ Some model details are unavailable due to dynamic input dimensions. "
                    "See section Input Tensor(s) Information below for more details."
                )
                model_summary.ui.warningLabel.show()

            elif not opt_passed:
                model_summary.ui.warningLabel.setText(
                    "⚠️ The model could not be optimized either due to an ONNX Runtime "
                    "session error or it did not pass the ONNX checker."
                )
                model_summary.ui.warningLabel.show()

            progress.step()
            progress.setLabelText("Checking for dynamic Inputs")

            self.ui.tabWidget.addTab(model_summary, "")
            model_summary.ui.flops.setText("Loading...")

            # Hide some of the components
            model_summary.ui.similarityCorrelation.hide()
            model_summary.ui.similarityCorrelationStatic.hide()

            model_summary.file = filepath
            model_summary.setObjectName(model_name)
            model_summary.ui.modelName.setText(model_name)
            model_summary.ui.modelFilename.setText(filepath)
            model_summary.ui.generatedDate.setText(datetime.now().strftime("%B %d, %Y"))

            self.digest_models[model_id].model_name = model_name
            self.digest_models[model_id].filepath = filepath

            self.digest_models[model_id].model_inputs = (
                onnx_utils.get_model_input_shapes_types(opt_model)
            )
            self.digest_models[model_id].model_outputs = (
                onnx_utils.get_model_output_shapes_types(opt_model)
            )

            progress.step()
            progress.setLabelText("Calculating Parameter Count")

            parameter_count = onnx_utils.get_parameter_count(opt_model)
            model_summary.ui.parameters.setText(format(parameter_count, ","))

            # Kick off model stats thread
            self.model_nodes_stats_thread[model_id] = StatsThread()
            self.model_nodes_stats_thread[model_id].completed.connect(
                self.update_flops_label
            )

            self.model_nodes_stats_thread[model_id].model = opt_model
            self.model_nodes_stats_thread[model_id].tab_name = model_name
            self.model_nodes_stats_thread[model_id].unique_id = model_id
            self.model_nodes_stats_thread[model_id].start()

            progress.step()
            progress.setLabelText("Calculating Node Type Counts")

            node_type_counts = onnx_utils.get_node_type_counts(opt_model)
            if len(node_type_counts) < 15:
                bar_spacing = 40
            else:
                bar_spacing = 20
            model_summary.ui.opHistogramChart.bar_spacing = bar_spacing
            model_summary.ui.opHistogramChart.set_data(node_type_counts)
            model_summary.ui.nodes.setText(str(sum(node_type_counts.values())))
            self.digest_models[model_id].node_type_counts = node_type_counts

            progress.step()
            progress.setLabelText("Gathering Model Inputs and Outputs")

            # Inputs Table
            model_summary.ui.inputsTable.setRowCount(
                len(self.digest_models[model_id].model_inputs)
            )

            for row_idx, (input_name, input_info) in enumerate(
                self.digest_models[model_id].model_inputs.items()
            ):
                model_summary.ui.inputsTable.setItem(
                    row_idx, 0, QTableWidgetItem(input_name)
                )
                model_summary.ui.inputsTable.setItem(
                    row_idx, 1, QTableWidgetItem(str(input_info.shape))
                )
                model_summary.ui.inputsTable.setItem(
                    row_idx, 2, QTableWidgetItem(str(input_info.dtype))
                )
                model_summary.ui.inputsTable.setItem(
                    row_idx, 3, QTableWidgetItem(str(input_info.size_kbytes))
                )

            model_summary.ui.inputsTable.resizeColumnsToContents()
            model_summary.ui.inputsTable.resizeRowsToContents()

            # Outputs Table
            model_summary.ui.outputsTable.setRowCount(
                len(self.digest_models[model_id].model_outputs)
            )
            for row_idx, (output_name, output_info) in enumerate(
                self.digest_models[model_id].model_outputs.items()
            ):
                model_summary.ui.outputsTable.setItem(
                    row_idx, 0, QTableWidgetItem(output_name)
                )
                model_summary.ui.outputsTable.setItem(
                    row_idx, 1, QTableWidgetItem(str(output_info.shape))
                )
                model_summary.ui.outputsTable.setItem(
                    row_idx, 2, QTableWidgetItem(str(output_info.dtype))
                )
                model_summary.ui.outputsTable.setItem(
                    row_idx, 3, QTableWidgetItem(str(output_info.size_kbytes))
                )

            model_summary.ui.outputsTable.resizeColumnsToContents()
            model_summary.ui.outputsTable.resizeRowsToContents()

            progress.step()
            progress.setLabelText("Gathering Model Proto Data")

            # ModelProto Info
            model_summary.ui.modelProtoTable.setItem(
                0, 1, QTableWidgetItem(str(opt_model.model_version))
            )
            self.digest_models[model_id].model_version = opt_model.model_version

            model_summary.ui.modelProtoTable.setItem(
                1, 1, QTableWidgetItem(str(opt_model.graph.name))
            )
            self.digest_models[model_id].graph_name = opt_model.graph.name

            producer_txt = f"{opt_model.producer_name} {opt_model.producer_version}"
            model_summary.ui.modelProtoTable.setItem(
                2, 1, QTableWidgetItem(producer_txt)
            )
            self.digest_models[model_id].producer_name = opt_model.producer_name
            self.digest_models[model_id].producer_version = opt_model.producer_version

            model_summary.ui.modelProtoTable.setItem(
                3, 1, QTableWidgetItem(str(opt_model.ir_version))
            )
            self.digest_models[model_id].ir_version = opt_model.ir_version

            for imp in opt_model.opset_import:
                row_idx = model_summary.ui.importsTable.rowCount()
                model_summary.ui.importsTable.insertRow(row_idx)
                if imp.domain == "" or imp.domain == "ai.onnx":
                    model_summary.ui.opsetVersion.setText(str(imp.version))
                    domain = "ai.onnx"
                    self.digest_models[model_id].opset = imp.version
                else:
                    domain = imp.domain
                model_summary.ui.importsTable.setItem(
                    row_idx, 0, QTableWidgetItem(str(domain))
                )
                model_summary.ui.importsTable.setItem(
                    row_idx, 1, QTableWidgetItem(str(imp.version))
                )
                row_idx += 1

                self.digest_models[model_id].imports[imp.domain] = imp.version

            progress.step()
            progress.setLabelText("Wrapping Up Model Analysis")

            model_summary.ui.importsTable.resizeColumnsToContents()
            model_summary.ui.modelProtoTable.resizeColumnsToContents()
            model_summary.setObjectName(model_name)
            new_tab_idx = self.ui.tabWidget.count() - 1
            self.ui.tabWidget.setTabText(new_tab_idx, "".join(model_name))
            self.ui.tabWidget.setCurrentIndex(new_tab_idx)
            self.ui.stackedWidget.setCurrentIndex(self.Page.SUMMARY)
            self.ui.singleModelWidget.show()
            progress.step()

            movie = QMovie(":/assets/gifs/load.gif")
            model_summary.ui.similarityImg.setMovie(movie)
            movie.start()

            # Start similarity Analysis
            # Note: Should only be started after the model tab has been created
            png_tmp_path = os.path.join(self.temp_dir.name, model_id)
            os.makedirs(png_tmp_path, exist_ok=True)
            self.model_similarity_thread[model_id] = SimilarityThread()
            self.model_similarity_thread[model_id].completed_successfully.connect(
                self.update_similarity_widget
            )
            self.model_similarity_thread[model_id].model_filepath = filepath
            self.model_similarity_thread[model_id].png_filepath = os.path.join(
                png_tmp_path, f"heatmap_{model_name}.png"
            )
            self.model_similarity_thread[model_id].model_id = model_id
            self.model_similarity_thread[model_id].start()

            progress.close()

        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(".onnx"):
                    self.load_onnx(file_path)
                    break

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

        digest_model = current_tab.digest_model
        if not digest_model.model_name:
            print("Warning, digest_model model name not set.")

        model_name = str(digest_model.model_name)

        save_directory = QFileDialog(self).getExistingDirectory(
            self, "Select Directory"
        )

        if not save_directory:
            return

        # Create a QDir object
        directory = QDir(save_directory)

        # Check if the directory exists and is writable
        if not directory.exists() and directory.isWritable():  # type: ignore
            self.show_warning_dialog(
                f"The directory {save_directory} is not valid or writable."
            )

        save_directory = os.path.join(
            save_directory, str(digest_model.model_name) + "_reports"
        )

        os.makedirs(save_directory, exist_ok=True)

        # Save the node histogram image
        node_histogram = current_tab.ui.opHistogramChart.grab()
        node_histogram.save(
            os.path.join(save_directory, f"{model_name}_histogram.png"), "PNG"
        )

        # Save csv of node type counts
        node_type_filepath = os.path.join(
            save_directory, f"{model_name}_node_type_counts.csv"
        )
        node_counter = digest_model.get_node_type_counts()
        if node_counter:
            onnx_utils.save_node_type_counts_csv_report(
                node_counter, node_type_filepath
            )

        # Save the similarity image
        similarity_png = self.model_similarity_report[digest_model.unique_id].grab()
        similarity_png.save(
            os.path.join(save_directory, f"{model_name}_heatmap.png"), "PNG"
        )

        # Save the text report
        txt_report_filepath = os.path.join(save_directory, f"{model_name}_report.txt")
        digest_model.save_txt_report(txt_report_filepath)

        # Save the node list
        nodes_report_filepath = os.path.join(save_directory, f"{model_name}_nodes.csv")
        self.save_nodes_csv(nodes_report_filepath, False)

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
            current_tab.digest_model.save_nodes_csv_report(csv_filepath)

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
        model_id = current_tab.digest_model.unique_id
        if model_id in self.nodes_window:
            del self.nodes_window[model_id]

        digest_models = self.digest_models[model_id]

        node_summary = NodeSummary(
            model_name=model_name, node_data=digest_models.per_node_info
        )

        self.nodes_window[model_id] = PopupWindow(
            node_summary, f"{model_name} Nodes Summary"
        )
        self.nodes_window[model_id].destroyed.connect(
            lambda: self.nodes_window.pop(model_id, None)
        )
        self.nodes_window[model_id].open()

    def closeEvent(self, event):
        for thread in self.model_nodes_stats_thread.values():
            thread.quit()  # Request the thread to stop
            thread.wait(5000)  # Wait for the thread to finish

        for thread in self.model_similarity_thread.values():
            thread.quit()  # Request the thread to stop
            thread.wait(5000)  # Wait for the thread to finish

        for window in QApplication.topLevelWidgets():
            if window != self:
                window.close()

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
