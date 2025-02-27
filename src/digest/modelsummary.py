# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

# pylint: disable=invalid-name
import os
from datetime import datetime
from typing import Optional

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtGui import QMovie
from PySide6.QtCore import QSize

from onnx import ModelProto

from digest.ui.modelsummary_ui import Ui_modelSummary
from digest.freeze_inputs import FreezeInputs
from digest.popup_window import PopupWindow
from digest.qt_utils import apply_dark_style_sheet
from digest.model_class.digest_model import SupportedModelTypes, DigestModel
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.model_class.digest_report_model import DigestReportModel


ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class modelSummary(QWidget):

    def __init__(self, digest_model: DigestModel, parent=None):
        super().__init__(parent)
        self.ui = Ui_modelSummary()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)

        self.file: Optional[str] = None
        self.ui.warningLabel.hide()
        self.model_id = digest_model.unique_id
        self.model_proto: Optional[ModelProto] = None
        model_name: str = digest_model.model_name if digest_model.model_name else ""

        self.png_file_path: Optional[str] = None
        self.load_gif = QMovie(":/assets/gifs/load.gif")
        # We set the size of the GIF to half the original
        self.load_gif.setScaledSize(QSize(214, 120))
        self.ui.similarityImg.setMovie(self.load_gif)
        self.load_gif.start()

        # There is no freezing if the model is not ONNX
        self.ui.freezeButton.setVisible(False)
        self.freeze_inputs: Optional[FreezeInputs] = None
        self.freeze_window: Optional[QWidget] = None

        self.model_type: Optional[SupportedModelTypes] = None

        if isinstance(digest_model, DigestOnnxModel):
            self.model_type = SupportedModelTypes.ONNX
            self.model_proto = (
                digest_model.model_proto if digest_model.model_proto else ModelProto()
            )
            self.freeze_inputs = FreezeInputs(self.model_proto, model_name)
            self.ui.freezeButton.clicked.connect(self.open_freeze_inputs)
            self.freeze_inputs.complete_signal.connect(self.close_freeze_window)
        elif isinstance(digest_model, DigestReportModel):
            self.model_type = SupportedModelTypes.REPORT

        # Hide some of the components
        self.ui.similarityCorrelation.hide()
        self.ui.similarityCorrelationStatic.hide()

        self.file = digest_model.filepath
        self.setObjectName(model_name)
        self.ui.modelName.setText(model_name)
        if self.file:
            self.ui.modelFilename.setText(self.file)

        self.ui.generatedDate.setText(datetime.now().strftime("%B %d, %Y"))

        self.ui.parameters.setText(format(digest_model.parameters, ","))

        node_type_counts = digest_model.node_type_counts
        if len(node_type_counts) < 15:
            bar_spacing = 40
        else:
            bar_spacing = 20
        self.ui.opHistogramChart.bar_spacing = bar_spacing
        self.ui.opHistogramChart.set_data(node_type_counts)
        self.ui.nodes.setText(str(sum(node_type_counts.values())))

        # Format flops with commas if available
        flops_str = "N/A"
        if digest_model.flops is not None:
            flops_str = format(digest_model.flops, ",")

            # Set up the FLOPs pie chart
            pie_chart_labels, pie_chart_data = zip(
                *digest_model.node_type_flops.items()
            )
            self.ui.flopsPieChart.set_data(
                "FLOPs Intensity Per Op Type",
                pie_chart_labels,
                pie_chart_data,
            )

            # Set up the params pie chart
            pie_chart_labels, pie_chart_data = zip(
                *digest_model.node_type_parameters.items()
            )
            self.ui.parametersPieChart.set_data(
                "Parameter Intensity Per Op Type",
                pie_chart_labels,
                pie_chart_data,
            )

        self.ui.flops.setText(flops_str)

        # Inputs Table
        self.ui.inputsTable.setRowCount(len(digest_model.model_inputs))

        for row_idx, (input_name, input_info) in enumerate(
            digest_model.model_inputs.items()
        ):
            self.ui.inputsTable.setItem(row_idx, 0, QTableWidgetItem(input_name))
            self.ui.inputsTable.setItem(
                row_idx, 1, QTableWidgetItem(str(input_info.shape))
            )
            self.ui.inputsTable.setItem(
                row_idx, 2, QTableWidgetItem(str(input_info.dtype))
            )
            self.ui.inputsTable.setItem(
                row_idx, 3, QTableWidgetItem(str(input_info.size_kbytes))
            )

        self.ui.inputsTable.resizeColumnsToContents()
        self.ui.inputsTable.resizeRowsToContents()

        # Outputs Table
        self.ui.outputsTable.setRowCount(len(digest_model.model_outputs))
        for row_idx, (output_name, output_info) in enumerate(
            digest_model.model_outputs.items()
        ):
            self.ui.outputsTable.setItem(row_idx, 0, QTableWidgetItem(output_name))
            self.ui.outputsTable.setItem(
                row_idx, 1, QTableWidgetItem(str(output_info.shape))
            )
            self.ui.outputsTable.setItem(
                row_idx, 2, QTableWidgetItem(str(output_info.dtype))
            )
            self.ui.outputsTable.setItem(
                row_idx, 3, QTableWidgetItem(str(output_info.size_kbytes))
            )

        self.ui.outputsTable.resizeColumnsToContents()
        self.ui.outputsTable.resizeRowsToContents()

        if isinstance(digest_model, DigestOnnxModel):

            if digest_model.model_version:
                # ModelProto Info
                self.ui.modelProtoTable.setItem(
                    0, 1, QTableWidgetItem(digest_model.model_version)
                )

            if digest_model.graph_name:
                self.ui.modelProtoTable.setItem(
                    1, 1, QTableWidgetItem(digest_model.graph_name)
                )

            producer_txt = (
                f"{digest_model.producer_name} {digest_model.producer_version}"
            )
            self.ui.modelProtoTable.setItem(2, 1, QTableWidgetItem(producer_txt))

            self.ui.modelProtoTable.setItem(
                3, 1, QTableWidgetItem(str(digest_model.ir_version))
            )

            for domain, version in digest_model.imports.items():
                row_idx = self.ui.importsTable.rowCount()
                self.ui.importsTable.insertRow(row_idx)
                if domain == "" or domain == "ai.onnx":
                    self.ui.opsetVersion.setText(str(version))
                    domain = "ai.onnx"
                self.ui.importsTable.setItem(row_idx, 0, QTableWidgetItem(domain))
                self.ui.importsTable.setItem(row_idx, 1, QTableWidgetItem(str(version)))
                row_idx += 1

        self.ui.importsTable.resizeColumnsToContents()
        self.ui.modelProtoTable.resizeColumnsToContents()
        self.setObjectName(model_name)

    def open_freeze_inputs(self):
        if self.freeze_inputs:
            self.freeze_window = PopupWindow(
                self.freeze_inputs, "Freeze Model Inputs", self
            )
            self.freeze_window.open()

    def close_freeze_window(self):
        if self.freeze_window:
            self.freeze_window.close()
