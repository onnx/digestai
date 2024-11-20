# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import sys
import importlib.metadata

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import (
    QPushButton,
    QDialog,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QTextEdit,
    QProgressDialog,
)

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class ProgressDialog(QProgressDialog):
    """A pop up window with a progress label that goes from 1 to 100"""

    def __init__(self, label: str, num_steps: int, parent=None):
        """
        label: the text to be shown in the pop up dialog
        num_steps: the total number of events the progress bar will load through
        """
        super().__init__(label, "Cancel", 1, num_steps, parent)

        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimumDuration(0)
        self.setWindowTitle("Digest")
        self.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))
        self.setValue(1)

        self.user_canceled = False
        self.canceled.connect(self.cancel)
        self.step_size = 1
        self.current_step = 0
        self.num_steps = num_steps

    def step(self):
        self.current_step += self.step_size
        if self.current_step > self.num_steps:
            self.current_step = self.num_steps
        self.setValue(self.current_step)

    def cancel(self):
        self.user_canceled = True


class InfoDialog(QDialog):
    """This is a specific dialog class used to display the package information
    when a user clicks the info button"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Information")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Application Version
        layout.addWidget(QLabel("<b>Digest Package Information</b>"))

        # Python Packages, if you add a new package please update the
        # main.spec file in the root_dir (just follow whats there for these packages)
        for package in [
            "digestai",
            "onnx",
            "onnxruntime",
        ]:  # Add relevant packages here
            version = importlib.metadata.version(package)
            layout.addWidget(QLabel(f"{package}: {version}"))
        major, minor, micro, _, _ = sys.version_info
        python_version_str = f"{major}.{minor}.{micro}"
        layout.addWidget(QLabel(f"Python: {python_version_str}"))

        self.setLayout(layout)


class StatusDialog(QDialog):
    """A pop up dialog window indicating some useful info the user"""

    def __init__(self, status_message: str, title: str = "", parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))

        # Modernization
        self.setWindowTitle(
            title or "Status Message"
        )  # Use title if provided, else default
        self.setWindowFlags(Qt.WindowType.Dialog)

        # Modal Behavior (takes over screen)
        self.setWindowModality(Qt.WindowModality.WindowModal)

        layout = QVBoxLayout()

        message_label = QTextEdit(status_message)
        message_label.setReadOnly(True)  # Prevent editing
        message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        message_label.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred
        )  # Allow the label to expand
        message_label.setMinimumWidth(300)
        message_label.setMaximumHeight(75)
        layout.addWidget(message_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # Close dialog when clicked
        layout.addWidget(ok_button)

        self.setLayout(layout)


class WarnDialog(QDialog):
    """A pop up dialog window indicating a warning to the user"""

    def __init__(self, warning_message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Warning Message")
        self.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Application Version
        layout.addWidget(QLabel("<b>Something went wrong</b>"))
        layout.addWidget(QLabel(warning_message))
        self.setLayout(layout)
