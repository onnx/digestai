# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
from collections import OrderedDict
from typing import Optional, Callable, Union, List
from platformdirs import user_cache_dir
import torch

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QFormLayout,
    QFileDialog,
    QHBoxLayout,
    QComboBox,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
from utils import onnx_utils
from digest.ui.pytorchingest_ui import Ui_pytorchIngest
from digest.qt_utils import apply_dark_style_sheet
from digest.model_class.digest_pytorch_model import (
    get_model_fwd_parameters,
    DigestPyTorchModel,
)

torch_tensor_types = {
    "torch.float16": torch.float16,
    "torch.float32": torch.float32,
    "torch.float64": torch.float64,
    "torch.uint8": torch.uint8,
    "torch.uint16": torch.uint16,
    "torch.uint32": torch.uint32,
    "torch.uint64": torch.uint64,
    "torch.int8": torch.int8,
    "torch.int16": torch.int16,
    "torch.int32": torch.int32,
    "torch.int64": torch.int64,
    "torch.bool": torch.bool,
}


class UserModelInputsForm:
    def __init__(self, form_layout: QFormLayout):
        self.form_layout = form_layout
        self.num_rows = 0

    def add_row(
        self,
        label_text: str,
        text_width: int,
        edit_finished_fnc: Optional[Callable] = None,
    ) -> int:

        # The label displays the tensor name
        font = QFont("Inter", 10)
        label = QLabel(f"{label_text}:")
        label.setContentsMargins(0, 0, 0, 0)
        label.setFont(font)

        # The combo box enables users to specify the tensor data type
        dtype_combo_box = QComboBox()
        for tensor_type in torch_tensor_types.keys():
            dtype_combo_box.addItem(tensor_type)
        dtype_combo_box.setCurrentIndex(1)  # float32 by default
        dtype_combo_box.currentIndexChanged.connect(edit_finished_fnc)

        # Line edit is where the user specifies the tensor shape
        line_edit = QLineEdit()
        line_edit.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        line_edit.setMinimumWidth(text_width)
        line_edit.setMinimumHeight(20)
        line_edit.setPlaceholderText("Set tensor shape here")
        if edit_finished_fnc:
            line_edit.editingFinished.connect(edit_finished_fnc)

        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        row_layout.setSpacing(5)
        row_layout.setObjectName(f"row{self.num_rows}_layout")
        row_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        row_layout.addWidget(dtype_combo_box, alignment=Qt.AlignmentFlag.AlignHCenter)
        row_layout.addWidget(line_edit, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.num_rows += 1
        self.form_layout.addRow(row_layout)

        return self.num_rows

    def get_row_tensor_name(self, row_idx: int) -> str:
        form_item = self.form_layout.itemAt(row_idx, QFormLayout.ItemRole.FieldRole)
        row_layout = form_item.layout()
        assert isinstance(row_layout, QHBoxLayout)
        line_edit_item = row_layout.itemAt(0)
        line_edit_widget = line_edit_item.widget()
        assert isinstance(line_edit_widget, QLabel)
        return line_edit_widget.text().split(":")[0]

    def get_row_tensor_dtype(self, row_idx: int) -> torch.dtype:
        form_item = self.form_layout.itemAt(row_idx, QFormLayout.ItemRole.FieldRole)
        row_layout = form_item.layout()
        combo_box = row_layout.itemAt(1)
        assert combo_box, "The combo box was not found which is unexpected!"
        combo_box_widget = combo_box.widget()
        assert isinstance(combo_box_widget, QComboBox)
        return torch_tensor_types[combo_box_widget.currentText()]

    def get_row_tensor_shape(self, row_idx: int) -> List[Union[str, int]]:
        shape_widget = self.get_row_tensor_shape_widget(row_idx)
        shape_str = shape_widget.text()
        shape_list: List[Union[str, int]] = []
        if not shape_str:
            return shape_list
        shape_list_str = shape_str.split(",")

        for dim in shape_list_str:
            dim = dim.strip()
            # Integer based shape
            if all(char.isdigit() for char in dim):
                shape_list.append(int(dim))
            # Symbolic shape
            else:
                shape_list.append(dim)
        return shape_list

    def get_row_tensor_shape_widget(self, row_idx: int) -> QLineEdit:
        form_item = self.form_layout.itemAt(row_idx, QFormLayout.ItemRole.FieldRole)
        row_layout = form_item.layout()
        line_edit_item = row_layout.itemAt(2)
        assert line_edit_item
        line_edit_widget = line_edit_item.widget()
        assert isinstance(line_edit_widget, QLineEdit)
        return line_edit_widget


class PyTorchIngest(QWidget):
    """PyTorchIngest is the pop up window that enables users to set static shapes and export
    PyTorch models to ONNX models."""

    # This enables the widget to close the parent window
    close_signal = Signal()

    def __init__(
        self,
        model_file: str,
        model_name: str,
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_pytorchIngest()
        self.ui.setupUi(self)
        apply_dark_style_sheet(self)

        self.ui.exportWarningLabel.hide()

        # We use a cache dir to save the exported ONNX model
        # Users have the option to choose a different location
        # if they wish to keep the exported model.
        user_cache_directory = user_cache_dir("digest")
        os.makedirs(user_cache_directory, exist_ok=True)
        self.save_directory: str = user_cache_directory

        self.ui.selectDirBtn.clicked.connect(self.select_directory)
        self.ui.exportOnnxBtn.clicked.connect(self.export_onnx)

        self.ui.modelName.setText(str(model_name))

        self.ui.modelFilename.setText(str(model_file))

        self.ui.foldingCheckBox.stateChanged.connect(self.on_checkbox_folding_changed)
        self.ui.exportParamsCheckBox.stateChanged.connect(
            self.on_checkbox_export_params_changed
        )

        self.digest_pytorch_model = DigestPyTorchModel(model_file, model_name)
        self.digest_pytorch_model.do_constant_folding = (
            self.ui.foldingCheckBox.isChecked()
        )
        self.digest_pytorch_model.export_params = (
            self.ui.exportParamsCheckBox.isChecked()
        )

        self.user_input_form = UserModelInputsForm(self.ui.inputsFormLayout)

        # Set up the opset form
        self.lowest_supported_opset = 7  # this requirement came from pytorch
        self.supported_opset_version = onnx_utils.get_supported_opset()
        self.ui.opsetLineEdit.setText(str(self.digest_pytorch_model.opset))
        self.ui.opsetInfoLabel.setStyleSheet("color: grey;")
        self.ui.opsetInfoLabel.setText(
            f"(accepted range is {self.lowest_supported_opset} - {self.supported_opset_version}):"
        )
        self.ui.opsetLineEdit.editingFinished.connect(self.update_opset_version)

        # Present each input in the forward function
        self.fwd_parameters = OrderedDict(get_model_fwd_parameters(model_file))
        for val in self.fwd_parameters.values():
            self.user_input_form.add_row(
                str(val),
                250,
                self.update_tensor_info,
            )

    def set_widget_invalid(self, widget: QWidget):
        widget.setStyleSheet("border: 1px solid red;")

    def set_widget_valid(self, widget: QWidget):
        widget.setStyleSheet("")

    def on_checkbox_folding_changed(self):
        self.digest_pytorch_model.do_constant_folding = (
            self.ui.foldingCheckBox.isChecked()
        )

    def on_checkbox_export_params_changed(self):
        self.digest_pytorch_model.export_params = (
            self.ui.exportParamsCheckBox.isChecked()
        )

    def select_directory(self):
        dir = QFileDialog(self).getExistingDirectory(self, "Select Directory")
        if os.path.exists(dir):
            self.save_directory = dir
            info_message = f"The ONNX model will be exported to {self.save_directory}"
            self.update_message_label(info_message=info_message)

    def update_message_label(
        self, info_message: Optional[str] = None, warn_message: Optional[str] = None
    ) -> None:
        if info_message:
            message = f"ℹ️ {info_message}"
        elif warn_message:
            message = f"⚠️ {warn_message}"

        self.ui.selectDirLabel.setText(message)

    def update_opset_version(self):
        opset_text_item = self.ui.opsetLineEdit.text()
        if all(char.isdigit() for char in opset_text_item):
            opset_text_item = int(opset_text_item)
            if (
                opset_text_item
                and opset_text_item < self.lowest_supported_opset
                or opset_text_item > self.supported_opset_version
            ):
                self.set_widget_invalid(self.ui.opsetLineEdit)
            else:
                self.digest_pytorch_model.opset = opset_text_item
                self.set_widget_valid(self.ui.opsetLineEdit)

    def update_tensor_info(self):
        """Because this is an external function to the UserInputFormWithInfo class
        we go through each input everytime there is an update."""
        for row_idx in range(self.user_input_form.form_layout.rowCount()):
            widget = self.user_input_form.get_row_tensor_shape_widget(row_idx)
            tensor_name = self.user_input_form.get_row_tensor_name(row_idx)
            tensor_dtype = self.user_input_form.get_row_tensor_dtype(row_idx)
            try:
                tensor_shape = self.user_input_form.get_row_tensor_shape(row_idx)
            except ValueError as err:
                print(f"Shape invalid: {err}")
                self.set_widget_invalid(widget)
            else:
                if tensor_name and tensor_shape:
                    self.set_widget_valid(widget)
                    self.digest_pytorch_model.input_tensor_info[tensor_name] = (
                        tensor_dtype,
                        tensor_shape,
                    )

    def export_onnx(self):
        onnx_file_path = os.path.join(
            self.save_directory, f"{self.digest_pytorch_model.model_name}.onnx"
        )
        try:
            self.digest_pytorch_model.export_to_onnx(onnx_file_path)
        except (ValueError, TypeError, RuntimeError) as err:
            self.ui.exportWarningLabel.setText(f"Failed to export ONNX: {err}")
            self.ui.exportWarningLabel.show()
        else:
            self.ui.exportWarningLabel.hide()
            self.close_widget()

    def close_widget(self):
        self.close_signal.emit()
        self.close()
