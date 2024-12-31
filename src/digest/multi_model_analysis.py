# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
from datetime import datetime
import csv
from typing import List, Dict, Union
from collections import Counter, defaultdict, OrderedDict

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
from PySide6.QtCore import Qt
from digest.dialog import ProgressDialog, StatusDialog
from digest.ui.multimodelanalysis_ui import Ui_multiModelAnalysis
from digest.histogramchartwidget import StackedHistogramWidget
from digest.qt_utils import apply_dark_style_sheet
from digest.model_class.digest_model import (
    NodeTypeCounts,
    NodeShapeCounts,
    save_node_shape_counts_csv_report,
    save_node_type_counts_csv_report,
)
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.model_class.digest_report_model import DigestReportModel
import utils.onnx_utils as onnx_utils

ROOT_FOLDER = os.path.dirname(__file__)


class MultiModelAnalysis(QWidget):
    """MultiModelAnalysis is the pop up window containing analysis of several models."""

    def __init__(
        self,
        model_list: List[Union[DigestOnnxModel, DigestReportModel]],
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_multiModelAnalysis()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)

        self.ui.saveCsvBtn.clicked.connect(self.save_reports)

        self.ui.individualCheckBox.stateChanged.connect(self.check_box_changed)
        self.ui.multiCheckBox.stateChanged.connect(self.check_box_changed)

        # For some reason setting alignments in designer lead to bugs in *ui.py files
        self.ui.opHistogramChart.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        if not model_list:
            return

        # Holds the data for node type counts across all models
        self.global_node_type_counter: Counter[str] = Counter()

        # Holds the data for node shape counts across all models
        self.global_node_shape_counter: NodeShapeCounts = defaultdict(Counter)

        # Holds the data for all models statistics
        self.global_model_data: Dict[str, Dict[str, Union[int, str, None]]] = {}

        progress = ProgressDialog("", len(model_list), self)

        header_labels = [
            "Model Name",
            "Model Type",
            "Opset",
            "Total Nodes",
            "Parameters",
            "FLOPs",
        ]
        self.ui.dataTable.setRowCount(len(model_list))
        self.ui.dataTable.setColumnCount(len(header_labels))
        self.ui.dataTable.setHorizontalHeaderLabels(header_labels)
        self.ui.dataTable.setSortingEnabled(False)

        for row, model in enumerate(model_list):

            item = QTableWidgetItem(str(model.model_name))
            self.ui.dataTable.setItem(row, 0, item)

            item = QTableWidgetItem(str(model.model_type.name))
            self.ui.dataTable.setItem(row, 1, item)

            if isinstance(model, DigestOnnxModel):
                item = QTableWidgetItem(str(model.opset))
            elif isinstance(model, DigestReportModel):
                item = QTableWidgetItem(str(model.model_data.get("opset", "")))

            self.ui.dataTable.setItem(row, 2, item)

            item = QTableWidgetItem(str(len(model.node_data)))
            self.ui.dataTable.setItem(row, 3, item)

            item = QTableWidgetItem(str(model.parameters))
            self.ui.dataTable.setItem(row, 4, item)

            item = QTableWidgetItem(str(model.flops))
            self.ui.dataTable.setItem(row, 5, item)

        self.ui.dataTable.resizeColumnsToContents()
        self.ui.dataTable.resizeRowsToContents()

        # Until we use the unique_id to represent the model contents we store
        # the entire model as the key so that we can store models that happen to have
        # the same name. There is a guarantee that the models will not be duplicates.
        node_type_counter: Dict[
            Union[DigestOnnxModel, DigestReportModel], NodeTypeCounts
        ] = {}

        for i, digest_model in enumerate(model_list):
            progress.step()
            progress.setLabelText(f"Analyzing model {digest_model.model_name}")

            if digest_model.model_name is None:
                digest_model.model_name = f"model_{i}"

            if isinstance(digest_model, DigestOnnxModel):
                opset = digest_model.opset
                if digest_model.model_proto:
                    dynamic_input_dims = onnx_utils.get_dynamic_input_dims(
                        digest_model.model_proto
                    )
                    if dynamic_input_dims:
                        print(
                            "Found the following non-static input dims in your model. "
                            "It is recommended to make all dims static before generating reports."
                        )
                        for dynamic_shape in dynamic_input_dims:
                            print(f"dim: {dynamic_shape}")

            elif isinstance(digest_model, DigestReportModel):
                opset = digest_model.model_data.get("opset", "")

            # Update the global model dictionary
            if digest_model.unique_id in self.global_model_data:
                print(
                    f"Warning! {digest_model.model_name} with id "
                    f"{digest_model.unique_id} has already been processed, "
                    "skipping the duplicate model."
                )
                continue

            self.global_model_data[digest_model.unique_id] = {
                "model_name": digest_model.model_name,
                "model_type": digest_model.model_type.name,
                "opset": opset,
                "parameters": digest_model.parameters,
                "flops": digest_model.flops,
            }

            if digest_model in node_type_counter:
                print(
                    f"Warning! {digest_model.model_name} with model type "
                    f"{digest_model.model_type.value} and id {digest_model.unique_id} "
                    "has already been added to the stacked histogram, skipping."
                )
                continue

            node_type_counter[digest_model] = digest_model.node_type_counts

            # Update global data structure for node type counter
            self.global_node_type_counter.update(node_type_counter[digest_model])

            node_shape_counts = digest_model.get_node_shape_counts()

            # Update global data structure for node shape counter
            for node_type, shape_counts in node_shape_counts.items():
                self.global_node_shape_counter[node_type].update(shape_counts)

        progress.close()

        self.ui.opHistogramChart.set_data(
            OrderedDict(self.global_node_type_counter.most_common()),
            title="Combined Op Histogram",
        )

        # Create stacked op histograms
        max_count = 0
        top_ops = [key for key, _ in self.global_node_type_counter.most_common(20)]
        for model, _ in node_type_counter.items():
            max_local = Counter(node_type_counter[model]).most_common()[0][1]
            if max_local > max_count:
                max_count = max_local
        for idx, model in enumerate(node_type_counter):
            stacked_histogram_widget = StackedHistogramWidget()
            ordered_dict = OrderedDict()
            model_counter = Counter(node_type_counter[model])
            for key in top_ops:
                ordered_dict[key] = model_counter.get(key, 0)
            title = "Stacked Op Histogram" if idx == 0 else ""
            stacked_histogram_widget.set_data(
                ordered_dict,
                model_name=model.model_name,
                y_max=max_count,
                title=title,
                set_ticks=False,
            )
            frame_layout = self.ui.stackedHistogramFrame.layout()
            if frame_layout:
                frame_layout.addWidget(stacked_histogram_widget)

        # Add a "ghost" histogram to allow us to set the x axis label vertically
        stacked_histogram_widget = StackedHistogramWidget()
        ordered_dict = OrderedDict({key: 1 for key in top_ops})
        stacked_histogram_widget.set_data(
            ordered_dict,
            model_name="_",
            y_max=max_count,
            set_ticks=True,
        )
        frame_layout = self.ui.stackedHistogramFrame.layout()
        if frame_layout:
            frame_layout.addWidget(stacked_histogram_widget)

        self.model_list = model_list

    def save_reports(self):
        """This function saves all available reports for the models that are opened
        in the multi-model analysis page."""

        base_directory = QFileDialog(self).getExistingDirectory(
            self, "Select Directory"
        )

        # Check if the directory exists and is writable
        if not os.path.exists(base_directory) or not os.access(base_directory, os.W_OK):
            bad_ext_dialog = StatusDialog(
                f"The directory {base_directory} is not valid or writable.",
                parent=self,
            )
            bad_ext_dialog.show()

        # Append a subdirectory to the save_directory so that all reports are co-located
        name_id = datetime.now().strftime("%Y%m%d%H%M%S")
        sub_directory = f"multi_model_reports_{name_id}"
        save_directory = os.path.join(base_directory, sub_directory)
        try:
            os.makedirs(save_directory)
        except OSError as os_err:
            bad_ext_dialog = StatusDialog(
                f"Failed to create {save_directory} with error {os_err}",
                parent=self,
            )
            bad_ext_dialog.show()

        save_individual_reports = self.ui.individualCheckBox.isChecked()
        save_multi_reports = self.ui.multiCheckBox.isChecked()

        if save_individual_reports:
            progress = ProgressDialog("Saving reports", len(self.model_list), self)

            for digest_model in self.model_list:
                progress.step()

                # Save the text report for the model
                summary_filepath = os.path.join(
                    save_directory, f"{digest_model.model_name}_summary.txt"
                )

                digest_model.save_text_report(summary_filepath)

                # Save csv of node type counts
                node_type_filepath = os.path.join(
                    save_directory, f"{digest_model.model_name}_node_type_counts.csv"
                )

                if digest_model.node_type_counts:
                    digest_model.save_node_type_counts_csv_report(node_type_filepath)

                # Save csv containing node shape counts per op_type
                node_shape_filepath = os.path.join(
                    save_directory, f"{digest_model.model_name}_node_shape_counts.csv"
                )
                digest_model.save_node_shape_counts_csv_report(node_shape_filepath)

                # Save csv containing all node-level information
                nodes_filepath = os.path.join(
                    save_directory, f"{digest_model.model_name}_nodes.csv"
                )
                digest_model.save_nodes_csv_report(nodes_filepath)

            progress.close()

        if save_multi_reports:

            # Save all the global model analysis reports
            if len(self.model_list) > 1:
                global_filepath = os.path.join(
                    save_directory, "global_node_type_counts.csv"
                )
                global_node_type_counter = NodeTypeCounts(
                    self.global_node_type_counter.most_common()
                )
                save_node_type_counts_csv_report(
                    global_node_type_counter, global_filepath
                )

                global_filepath = os.path.join(
                    save_directory, "global_node_shape_counts.csv"
                )
                save_node_shape_counts_csv_report(
                    self.global_node_shape_counter, global_filepath
                )

                global_filepath = os.path.join(
                    save_directory, "global_model_summary.csv"
                )
                with open(
                    global_filepath, "w", newline="", encoding="utf-8"
                ) as csvfile:
                    writer = csv.writer(csvfile)
                    rows = [
                        [
                            data["model_name"],
                            data["model_type"],
                            data["opset"],
                            data["parameters"],
                            data["flops"],
                        ]
                        for _, data in self.global_model_data.items()
                    ]
                    writer.writerow(
                        ["Model Name", "Model Type", "Opset", "Parameters", "FLOPs"]
                    )
                    writer.writerows(rows)

        if save_individual_reports or save_multi_reports:
            StatusDialog(f"Saved reports to {save_directory}")

    def check_box_changed(self):
        if self.ui.individualCheckBox.isChecked() or self.ui.multiCheckBox.isChecked():
            self.ui.saveCsvBtn.setEnabled(True)
        else:
            self.ui.saveCsvBtn.setEnabled(False)
