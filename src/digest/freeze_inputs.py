# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
from datetime import datetime
import copy
from typing import Dict, List, Optional
from platformdirs import user_cache_dir

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QLayoutItem,
    QFormLayout,
    QFileDialog,
)
from PySide6.QtCore import Signal
from onnx import ModelProto, save, shape_inference, checker
import onnxruntime.tools.make_dynamic_shape_fixed as ort_fixed
from digest.ui.freezeinputs_ui import Ui_freezeInputs
from digest.dialog import ProgressDialog
from digest.qt_utils import apply_dark_style_sheet
from utils import onnx_utils

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class ModernLineEdit(QLineEdit):
    def __init__(self, text_changed_fnc=None):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMaximumWidth(50)
        self.textChanged.connect(text_changed_fnc)


class FreezeInputs(QWidget):
    """FreezeInputs is the pop up window that enables users to apply static values
    to dynamic dims."""

    complete_signal: Signal = Signal(str)

    def __init__(
        self,
        model_proto: ModelProto,
        model_name: str,
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_freezeInputs()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)

        self.ui.warningLabel.hide()

        user_cache_directory = user_cache_dir("digest")
        os.makedirs(user_cache_directory, exist_ok=True)
        self.save_directory: str = user_cache_directory

        self.model_name = model_name
        self.model_proto = model_proto
        self.proto_copy = copy.deepcopy(model_proto)

        self.ui.selectDirBtn.setEnabled(True)
        self.ui.applyShapesBtn.setEnabled(False)
        self.ui.applyShapesBtn.clicked.connect(self.apply_static_shapes)
        self.ui.selectDirBtn.clicked.connect(self.select_directory)

        info_message = (
            f"The static model will be saved to {self.save_directory} "
            "once you apply the shapes below."
        )
        self.update_message_label(info_message=info_message)

        self.dynamic_inputs: List[str] = []

        # Dynamic dims form
        dynamic_inputs = onnx_utils.get_dynamic_input_dims(model_proto)
        for dynamic_input in dynamic_inputs:
            label = QLabel(dynamic_input)
            line_edit = ModernLineEdit(self.check_form_complete)
            self.ui.formLayout.addRow(label, line_edit)

        model_inputs = onnx_utils.get_model_input_shapes_types(model_proto)
        self.update_inputs_table(model_inputs)

        try:
            checker.check_model(model_proto, full_check=True)
        except checker.ValidationError as exp:
            print(f"Model did not pass checker: {exp}")
            self.show_warning_and_disable_page()

    def select_directory(self):
        dir = QFileDialog(self).getExistingDirectory(self, "Select Directory")
        if dir:
            self.save_directory = dir
            info_message = (
                f"The static model will be saved to {self.save_directory} "
                "once you apply the shapes below."
            )
            self.update_message_label(info_message=info_message)

    def update_message_label(
        self, info_message: Optional[str] = None, warn_message: Optional[str] = None
    ) -> None:
        if info_message:
            message = f"ℹ️ {info_message}"
        elif warn_message:
            message = f"⚠️ {warn_message}"

        self.ui.selectDirLabel.setText(message)

    def update_inputs_table(self, model_inputs: onnx_utils.TensorData):
        # Inputs Table
        self.ui.inputsTable.setRowCount(len(model_inputs))

        for row_idx, (input_name, input_info) in enumerate(model_inputs.items()):
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

    def check_form_complete(self):
        for i in range(self.ui.formLayout.count()):
            item = self.ui.formLayout.itemAt(i)
            if isinstance(item, QLayoutItem) and item.widget() is not None:
                widget = item.widget()
                if isinstance(widget, QLineEdit) and not widget.text().strip():
                    self.ui.applyShapesBtn.setEnabled(False)
                    return

        self.ui.applyShapesBtn.setEnabled(True)

    def apply_static_shapes(self) -> None:

        status = ProgressDialog(
            "Applying static shapes...",
            self.ui.formLayout.rowCount() + len(self.model_proto.graph.input),
        )
        status.show()

        # Given the enable feature of the apply shapes button we are guaranteed
        # to arrive in this function with shapes for each dynamic dim.
        dims: Dict[str, int] = {}
        for i in range(self.ui.formLayout.rowCount()):
            if status.wasCanceled():
                break
            status.step()
            label_item = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.LabelRole)
            field_item = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole)
            if label_item and field_item:
                label = label_item.widget()
                line_edit = field_item.widget()
                if isinstance(label, QLabel) and isinstance(line_edit, QLineEdit):
                    label_text = label.text()
                    line_edit_value = int(line_edit.text())
                    dims[label_text] = line_edit_value

        for tensor in self.model_proto.graph.input:
            if status.wasCanceled():
                break
            status.step()
            tensor_shape = []
            for dim in tensor.type.tensor_type.shape.dim:
                if dim.dim_param in dims:
                    tensor_shape.append(dims[dim.dim_param])
                elif dim.dim_value:
                    tensor_shape.append(dim.dim_value)

            ort_fixed.make_input_shape_fixed(
                self.proto_copy.graph, tensor.name, tensor_shape
            )

        try:
            inferred_model = shape_inference.infer_shapes(
                self.proto_copy, strict_mode=True, data_prop=True
            )
            status.setLabelText("Saving static model")
            name_id = datetime.now().strftime("%Y%m%d%H%M%S")
            static_model_filename = f"{self.model_name}_static_{name_id}.onnx"
            static_model_filepath = os.path.join(
                self.save_directory, static_model_filename
            )
            save(inferred_model, static_model_filepath)
            # We re-copy over the static model so that the user can create another variant
            self.proto_copy = copy.deepcopy(self.model_proto)
            status.setLabelText("Opening static model")
            self.complete_signal.emit(static_model_filepath)
        except checker.ValidationError as e:
            self.show_warning_and_disable_page()
            print(f"Model did not pass checker: {e}")
            status.close()

    def show_warning_and_disable_page(self):
        self.ui.warningLabel.show()
        for i in range(self.ui.formLayout.rowCount()):
            field_item = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole)
            if field_item:
                line_edit = field_item.widget()
                if isinstance(line_edit, QLineEdit):
                    line_edit.setEnabled(False)
