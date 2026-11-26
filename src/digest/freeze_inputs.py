# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
from datetime import datetime
import copy
import logging
from typing import Dict, List, Optional
from platformdirs import user_cache_dir

from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QFormLayout,
    QFileDialog,
)
from PySide6.QtCore import Signal
from onnx import ModelProto, save, shape_inference, checker
import onnxruntime.tools.make_dynamic_shape_fixed as ort_fixed
from digest.ui.freezeinputs_ui import Ui_freezeInputs
from digest.dialog import ProgressDialog
from digest.qt_utils import apply_dark_style_sheet
from digest.utils import onnx_utils

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGGER = logging.getLogger(__name__)


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
        self.save_directory: str = user_cache_directory

        self.model_name = model_name
        self.model_proto = model_proto
        self.model_is_valid = True

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
            LOGGER.warning("Model did not pass checker: %s", exp)
            self.model_is_valid = False
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
        try:
            self.read_dimensions()
        except ValueError:
            self.ui.applyShapesBtn.setEnabled(False)
        else:
            self.ui.applyShapesBtn.setEnabled(self.model_is_valid)

    def read_dimensions(self) -> Dict[str, int]:
        dims = {}
        for i in range(self.ui.formLayout.rowCount()):
            label = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
            field = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
            text = field.text().strip()
            if not text.isascii() or not text.isdecimal() or not 0 < int(text) < 2**63:
                raise ValueError("Enter a positive integer for every dynamic dimension.")
            dims[label.text()] = int(text)
        return dims

    def apply_static_shapes(self) -> None:
        if not self.model_is_valid:
            return
        try:
            dims = self.read_dimensions()
        except ValueError as error:
            self.update_message_label(warn_message=str(error))
            return

        # Every attempt starts from the original model, including retries after
        # cancellation or failed shape inference.
        proto_copy = copy.deepcopy(self.model_proto)
        status = ProgressDialog(
            "Applying static shapes...",
            len(self.model_proto.graph.input) + 2,
            self,
        )
        status.show()
        self.ui.applyShapesBtn.setEnabled(False)
        try:
            for tensor in self.model_proto.graph.input:
                status.step()
                if status.wasCanceled():
                    return
                tensor_shape = []
                for dim in tensor.type.tensor_type.shape.dim:
                    if dim.dim_param in dims:
                        tensor_shape.append(dims[dim.dim_param])
                    elif dim.HasField("dim_value"):
                        tensor_shape.append(dim.dim_value)
                    else:
                        raise ValueError("An unnamed dynamic dimension cannot be frozen.")
                ort_fixed.make_input_shape_fixed(proto_copy.graph, tensor.name, tensor_shape)

            inferred_model = shape_inference.infer_shapes(
                proto_copy, strict_mode=True, data_prop=True
            )
            checker.check_model(inferred_model, full_check=True)
            status.step()
            if status.wasCanceled():
                return
            status.setLabelText("Saving static model")
            name_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
            static_model_filename = f"{self.model_name}_static_{name_id}.onnx"
            static_model_filepath = os.path.join(
                self.save_directory, static_model_filename
            )
            os.makedirs(self.save_directory, exist_ok=True)
            save(inferred_model, static_model_filepath)
            self.update_message_label(info_message=f"Saved static model to {static_model_filepath}")
            status.setLabelText("Opening static model")
            self.complete_signal.emit(static_model_filepath)
        except Exception as error:  # noqa: BLE001 -- report failures at the GUI boundary
            LOGGER.exception("Failed to freeze model %s", self.model_name)
            self.update_message_label(warn_message=f"Could not freeze the model: {error}")
        finally:
            status.close()
            self.check_form_complete()

    def show_warning_and_disable_page(self):
        self.ui.warningLabel.show()
        self.ui.applyShapesBtn.setEnabled(False)
        for i in range(self.ui.formLayout.rowCount()):
            field_item = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole)
            if field_item:
                line_edit = field_item.widget()
                if isinstance(line_edit, QLineEdit):
                    line_edit.setEnabled(False)
