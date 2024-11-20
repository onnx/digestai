# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import csv
from typing import List, Dict, Union
from collections import Counter, defaultdict, OrderedDict

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
from digest.dialog import ProgressDialog, StatusDialog
from digest.ui.multimodelanalysis_ui import Ui_multiModelAnalysis
from digest.histogramchartwidget import StackedHistogramWidget
from digest.qt_utils import apply_dark_style_sheet
from utils import onnx_utils

ROOT_FOLDER = os.path.dirname(__file__)


class MultiModelAnalysis(QWidget):
    """MultiModelAnalysis is the pop up window containing analysis of several models."""

    def __init__(
        self,
        model_list: List[onnx_utils.DigestOnnxModel],
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_multiModelAnalysis()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)

        self.ui.saveCsvBtn.clicked.connect(self.save_reports)

        self.ui.individualCheckBox.stateChanged.connect(self.check_box_changed)
        self.ui.multiCheckBox.stateChanged.connect(self.check_box_changed)

        if not model_list:
            return

        # Holds the data for node type counts across all models
        self.global_node_type_counter: Counter[str] = Counter()

        # Holds the data for node shape counts across all models
        self.global_node_shape_counter: onnx_utils.NodeShapeCounts = defaultdict(
            Counter
        )

        # Holds the data for all models statistics
        self.global_model_data: Dict[str, Dict[str, Union[int, None]]] = {}

        progress = ProgressDialog("", len(model_list), self)

        header_labels = ["Model", "Opset", "Total Nodes", "Parameters", "FLOPs"]
        self.ui.dataTable.setRowCount(len(model_list))
        self.ui.dataTable.setColumnCount(len(header_labels))
        self.ui.dataTable.setHorizontalHeaderLabels(header_labels)
        self.ui.dataTable.setSortingEnabled(False)

        for row, model in enumerate(model_list):
            item = QTableWidgetItem(str(model.model_name))
            self.ui.dataTable.setItem(row, 0, item)

            item = QTableWidgetItem(str(model.opset))
            self.ui.dataTable.setItem(row, 1, item)

            item = QTableWidgetItem(str(len(model.per_node_info)))
            self.ui.dataTable.setItem(row, 2, item)

            item = QTableWidgetItem(str(model.model_parameters))
            self.ui.dataTable.setItem(row, 3, item)

            item = QTableWidgetItem(str(model.model_flops))
            self.ui.dataTable.setItem(row, 4, item)

        self.ui.dataTable.resizeColumnsToContents()
        self.ui.dataTable.resizeRowsToContents()

        node_type_counter = {}
        for i, digest_model in enumerate(model_list):
            progress.step()
            progress.setLabelText(f"Analyzing model {digest_model.model_name}")

            if digest_model.model_name is None:
                digest_model.model_name = f"model_{i}"

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

            # Update the global model dictionary
            if digest_model.model_name in self.global_model_data:
                print(
                    f"Warning! {digest_model.model_name} has already been processed, "
                    "skipping the duplicate model."
                )

            self.global_model_data[digest_model.model_name] = {
                "opset": digest_model.opset,
                "parameters": digest_model.model_parameters,
                "flops": digest_model.model_flops,
            }

            node_type_counter[digest_model.model_name] = (
                digest_model.get_node_type_counts()
            )

            # Update global data structure for node type counter
            self.global_node_type_counter.update(
                node_type_counter[digest_model.model_name]
            )

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
        for model_name, _ in node_type_counter.items():
            max_local = Counter(node_type_counter[model_name]).most_common()[0][1]
            if max_local > max_count:
                max_count = max_local
        for idx, model_name in enumerate(node_type_counter):
            stacked_histogram_widget = StackedHistogramWidget()
            ordered_dict = OrderedDict()
            model_counter = Counter(node_type_counter[model_name])
            for key in top_ops:
                ordered_dict[key] = model_counter.get(key, 0)
            title = "Stacked Op Histogram" if idx == 0 else ""
            stacked_histogram_widget.set_data(
                ordered_dict,
                model_name=model_name,
                y_max=max_count,
                title=title,
                set_ticks=False,
            )
            frame_layout = self.ui.stackedHistogramFrame.layout()
            frame_layout.addWidget(stacked_histogram_widget)

        # Add a "ghost" histogram to allow us to set the x axis label vertically
        model_name = list(node_type_counter.keys())[0]
        stacked_histogram_widget = StackedHistogramWidget()
        ordered_dict = {key: 1 for key in top_ops}
        stacked_histogram_widget.set_data(
            ordered_dict,
            model_name="_",
            y_max=max_count,
            set_ticks=True,
        )
        frame_layout = self.ui.stackedHistogramFrame.layout()
        frame_layout.addWidget(stacked_histogram_widget)

        self.model_list = model_list

    def save_reports(self):
        # Model summary text report
        save_directory = QFileDialog(self).getExistingDirectory(
            self, "Select Directory"
        )

        if not save_directory:
            return

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

                digest_model.save_txt_report(summary_filepath)

                # Save csv of node type counts
                node_type_filepath = os.path.join(
                    save_directory, f"{digest_model.model_name}_node_type_counts.csv"
                )

                # Save csv containing node type counter
                node_type_counter = digest_model.get_node_type_counts()

                if node_type_counter:
                    onnx_utils.save_node_type_counts_csv_report(
                        node_type_counter, node_type_filepath
                    )

                # Save csv containing node shape counts per op_type
                node_shape_counts = digest_model.get_node_shape_counts()
                node_shape_filepath = os.path.join(
                    save_directory, f"{digest_model.model_name}_node_shape_counts.csv"
                )
                onnx_utils.save_node_shape_counts_csv_report(
                    node_shape_counts, node_shape_filepath
                )

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
                global_node_type_counter = onnx_utils.NodeTypeCounts(
                    self.global_node_type_counter.most_common()
                )
                onnx_utils.save_node_type_counts_csv_report(
                    global_node_type_counter, global_filepath
                )

                global_filepath = os.path.join(
                    save_directory, "global_node_shape_counts.csv"
                )
                onnx_utils.save_node_shape_counts_csv_report(
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
                        [model, data["opset"], data["parameters"], data["flops"]]
                        for model, data in self.global_model_data.items()
                    ]
                    writer.writerow(["Model", "Opset", "Parameters", "FLOPs"])
                    writer.writerows(rows)

        if save_individual_reports or save_multi_reports:
            StatusDialog(f"Saved reports to {save_directory}")

    def check_box_changed(self):
        if self.ui.individualCheckBox.isChecked() or self.ui.multiCheckBox.isChecked():
            self.ui.saveCsvBtn.setEnabled(True)
        else:
            self.ui.saveCsvBtn.setEnabled(False)
