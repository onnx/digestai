# Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.

import os

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
from digest.ui.nodessummary_ui import Ui_nodesSummary
from digest.qt_utils import apply_dark_style_sheet
from digest.model_class.digest_model import (
    save_node_shape_counts_csv_report,
    save_nodes_csv_report,
)
from utils import onnx_utils

ROOT_FOLDER = os.path.dirname(__file__)


class NodeSummary(QWidget):
    """NodeSummary is the pop up window when a user clicks the Node List icon."""

    def __init__(
        self,
        model_name: str,
        node_data: onnx_utils.NodeData,
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_nodesSummary()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)
        self.ui.saveCsvBtn.clicked.connect(self.save_csv_file)
        self.node_data = node_data
        self.ui.modelName.setText(model_name)
        self.node_shape_counts = onnx_utils.get_node_shape_counts(node_data)
        self.ui.allNodesBtn.clicked.connect(self.update_table)
        self.ui.shapeCountsBtn.clicked.connect(self.update_table)
        self.update_table()

    def update_table(self):

        if self.ui.allNodesBtn.isChecked():
            header_labels = [
                "Node Name",
                "Node Type",
                "Parameters",
                "FLOPs",
                "Input Shapes",
                "Output Shapes",
                "Attributes",
            ]
            self.ui.dataTable.setRowCount(len(self.node_data))
            self.ui.dataTable.setColumnCount(len(header_labels))
            self.ui.dataTable.setHorizontalHeaderLabels(header_labels)
            self.ui.dataTable.setSortingEnabled(True)

            for row, node_name in enumerate(self.node_data.keys()):
                item = QTableWidgetItem(str(node_name))
                self.ui.dataTable.setItem(row, 0, item)
                node_info = self.node_data[node_name]

                input_shapes = [
                    tensor_info.shape for tensor_info in node_info.inputs.values()
                ]

                output_shapes = [
                    tensor_info.shape for tensor_info in node_info.inputs.values()
                ]

                data = [
                    node_info.node_type,
                    node_info.parameters,
                    node_info.flops,
                    input_shapes,
                    output_shapes,
                ]

                if node_info.attributes:
                    data.append(str({k: v for k, v in node_info.attributes.items()}))
                else:
                    data.append("")

                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    self.ui.dataTable.setItem(row, col + 1, item)

        elif self.ui.shapeCountsBtn.isChecked():
            header_labels = [
                "Node Type",
                "Input Shapes",
                "Count",
            ]

            total_rows = sum([len(entry) for entry in self.node_shape_counts.values()])
            self.ui.dataTable.setRowCount(total_rows)
            self.ui.dataTable.setColumnCount(len(header_labels))
            self.ui.dataTable.setHorizontalHeaderLabels(header_labels)

            row = 0
            for op_type, op_info in self.node_shape_counts.items():
                type_item = QTableWidgetItem(str(op_type))
                for shape, count in op_info.items():
                    self.ui.dataTable.setItem(row, 0, type_item)
                    item = QTableWidgetItem(str(shape))
                    self.ui.dataTable.setItem(row, 1, item)
                    item = QTableWidgetItem(str(count))
                    self.ui.dataTable.setItem(row, 2, item)
                    row += 1
                    type_item = QTableWidgetItem(str(""))

        self.ui.dataTable.resizeColumnsToContents()
        self.ui.dataTable.resizeRowsToContents()

    def save_csv_file(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", os.getcwd(), "CSV(*.csv)"
        )
        if filepath and self.ui.allNodesBtn.isChecked():
            save_nodes_csv_report(self.node_data, filepath)
        elif filepath and self.ui.shapeCountsBtn.isChecked():
            save_node_shape_counts_csv_report(self.node_shape_counts, filepath)
