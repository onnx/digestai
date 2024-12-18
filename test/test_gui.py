# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import sys
import tempfile
import unittest
from unittest.mock import patch
import timm
import torch

# pylint: disable=no-name-in-module
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

import digest.main
from digest.node_summary import NodeSummary
from digest.model_class.digest_pytorch_model import DigestPyTorchModel
from digest.pytorch_ingest import PyTorchIngest


def save_resnet18_pt(directory: str) -> str:
    """Simply saves a PyTorch resnet18 model and returns its file path"""
    model = timm.models.create_model("resnet18", pretrained=True)  # type: ignore
    model.eval()
    file_path = os.path.join(directory, "resnet18.pt")
    # Save the model
    try:
        torch.save(model, file_path)
        return file_path
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error saving model: {e}")
        return ""


class DigestGuiTest(unittest.TestCase):
    RESNET18_BASENAME = "resnet18"

    TEST_DIR = os.path.abspath(os.path.dirname(__file__))
    ONNX_FILE_PATH = os.path.normpath(
        os.path.join(TEST_DIR, f"{RESNET18_BASENAME}.onnx")
    )
    YAML_FILE_PATH = os.path.normpath(
        os.path.join(
            TEST_DIR, f"{RESNET18_BASENAME}_reports", f"{RESNET18_BASENAME}_report.yaml"
        )
    )

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if isinstance(cls.app, QApplication):
            cls.app.closeAllWindows()
        cls.app = None

    def setUp(self):
        self.digest_app = digest.main.DigestApp()
        self.digest_app.show()

    def tearDown(self):
        self.digest_app.close()

    def wait_all_threads(self, timeout=10000) -> bool:
        all_threads = list(self.digest_app.model_nodes_stats_thread.values()) + list(
            self.digest_app.model_similarity_thread.values()
        )

        for thread in all_threads:
            thread.wait(timeout)

        # Return True if all threads finished, False if timed out
        return all(thread.isFinished() for thread in all_threads)

    def test_open_valid_onnx(self):
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            mock_dialog.return_value = (
                self.ONNX_FILE_PATH,
                "",
            )

            num_tabs_prior = self.digest_app.ui.tabWidget.count()

            QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)

            self.assertTrue(self.wait_all_threads())

            self.assertTrue(
                self.digest_app.ui.tabWidget.count() == num_tabs_prior + 1
            )  # Check if a tab was added

            self.digest_app.closeTab(num_tabs_prior)

    def test_open_valid_yaml(self):
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            mock_dialog.return_value = (
                self.YAML_FILE_PATH,
                "",
            )

            num_tabs_prior = self.digest_app.ui.tabWidget.count()

            QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)

            self.assertTrue(self.wait_all_threads())

            self.assertTrue(
                self.digest_app.ui.tabWidget.count() == num_tabs_prior + 1
            )  # Check if a tab was added

            self.digest_app.closeTab(num_tabs_prior)

    def test_open_valid_pytorch(self):
        """We test the PyTorch path slightly different than the others
        since Digest opens a modal window that blocks the main thread. This makes it difficult
        to interact with the Window in this test."""

        with tempfile.TemporaryDirectory() as tmpdir:
            pt_file_path = save_resnet18_pt(tmpdir)
            self.assertTrue(os.path.exists(tmpdir))
            basename = os.path.splitext(os.path.basename(pt_file_path))
            model_name = basename[0]
            digest_model = DigestPyTorchModel(pt_file_path, model_name)
            self.assertTrue(isinstance(digest_model.file_path, str))
            pytorch_ingest = PyTorchIngest(pt_file_path, digest_model.model_name)
            pytorch_ingest.show()

            input_shape_edit = (
                pytorch_ingest.user_input_form.get_row_tensor_shape_widget(0)
            )

            assert input_shape_edit
            input_shape_edit.setText("batch_size, 3, 224, 224")
            pytorch_ingest.update_tensor_info()

            with patch(
                "PySide6.QtWidgets.QFileDialog.getExistingDirectory"
            ) as mock_save_dialog:
                print("TMPDIR", tmpdir)
                mock_save_dialog.return_value = tmpdir
                pytorch_ingest.select_directory()

            pytorch_ingest.ui.exportOnnxBtn.click()

            timeout_ms = 10000
            interval_ms = 100
            for _ in range(timeout_ms // interval_ms):
                QTest.qWait(interval_ms)
                onnx_file_path = pytorch_ingest.digest_pytorch_model.onnx_file_path
                if onnx_file_path and os.path.exists(onnx_file_path):
                    break  # File found!

            assert isinstance(pytorch_ingest.digest_pytorch_model.onnx_file_path, str)
            self.assertTrue(
                os.path.exists(pytorch_ingest.digest_pytorch_model.onnx_file_path)
            )

    def test_open_invalid_file(self):
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            mock_dialog.return_value = ("invalid_file.txt", "")
            num_tabs_prior = self.digest_app.ui.tabWidget.count()
            QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)
            self.assertTrue(self.wait_all_threads())
            self.assertEqual(self.digest_app.ui.tabWidget.count(), num_tabs_prior)

    def test_save_reports(self):
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName"
        ) as mock_open_dialog, patch(
            "PySide6.QtWidgets.QFileDialog.getExistingDirectory"
        ) as mock_save_dialog:

            mock_open_dialog.return_value = (self.ONNX_FILE_PATH, "")
            with tempfile.TemporaryDirectory() as tmpdirname:
                mock_save_dialog.return_value = tmpdirname

                QTest.mouseClick(
                    self.digest_app.ui.openFileBtn,
                    Qt.MouseButton.LeftButton,
                )

                self.assertTrue(self.wait_all_threads())

                self.assertTrue(
                    self.digest_app.ui.saveBtn.isEnabled(), "Save button is disabled!"
                )

                QTest.mouseClick(self.digest_app.ui.saveBtn, Qt.MouseButton.LeftButton)

                mock_save_dialog.assert_called_once()

                result_basepath = os.path.join(
                    tmpdirname, f"{self.RESNET18_BASENAME}_reports"
                )

                # Text report test
                text_report_FILE_PATH = os.path.join(
                    result_basepath, f"{self.RESNET18_BASENAME}_report.txt"
                )
                self.assertTrue(
                    os.path.isfile(text_report_FILE_PATH),
                    f"{text_report_FILE_PATH} not found!",
                )

                # YAML report test
                yaml_report_FILE_PATH = os.path.join(
                    result_basepath, f"{self.RESNET18_BASENAME}_report.yaml"
                )
                self.assertTrue(os.path.isfile(yaml_report_FILE_PATH))

                # Nodes test
                nodes_csv_report_FILE_PATH = os.path.join(
                    result_basepath, f"{self.RESNET18_BASENAME}_nodes.csv"
                )
                self.assertTrue(os.path.isfile(nodes_csv_report_FILE_PATH))

                # Histogram test
                histogram_FILE_PATH = os.path.join(
                    result_basepath, f"{self.RESNET18_BASENAME}_histogram.png"
                )
                self.assertTrue(os.path.isfile(histogram_FILE_PATH))

                # Heatmap test
                heatmap_FILE_PATH = os.path.join(
                    result_basepath, f"{self.RESNET18_BASENAME}_heatmap.png"
                )
                self.assertTrue(os.path.isfile(heatmap_FILE_PATH))

                num_tabs = self.digest_app.ui.tabWidget.count()
                self.assertTrue(num_tabs == 1)
                self.digest_app.closeTab(0)

    def test_save_tables(self):
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName"
        ) as mock_open_dialog, patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName"
        ) as mock_save_dialog:

            mock_open_dialog.return_value = (self.ONNX_FILE_PATH, "")
            with tempfile.TemporaryDirectory() as tmpdirname:
                mock_save_dialog.return_value = (
                    os.path.join(tmpdirname, f"{self.RESNET18_BASENAME}_nodes.csv"),
                    "",
                )

                QTest.mouseClick(
                    self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton
                )

                self.assertTrue(self.wait_all_threads())

                QTest.mouseClick(
                    self.digest_app.ui.nodesListBtn, Qt.MouseButton.LeftButton
                )

                # We assume there is only one model loaded
                _, node_window = self.digest_app.nodes_window.popitem()
                node_summary = node_window.main_window.centralWidget()

                self.assertIsInstance(node_summary, NodeSummary)

                # This line of code seems redundant but we do this to clean pylance
                if isinstance(node_summary, NodeSummary):
                    QTest.mouseClick(
                        node_summary.ui.saveCsvBtn, Qt.MouseButton.LeftButton
                    )

                    mock_save_dialog.assert_called_once()

                self.assertTrue(
                    os.path.exists(
                        os.path.join(tmpdirname, f"{self.RESNET18_BASENAME}_nodes.csv")
                    ),
                    "Nodes csv file not found.",
                )

                num_tabs = self.digest_app.ui.tabWidget.count()
                self.assertTrue(num_tabs == 1)
                self.digest_app.closeTab(0)


if __name__ == "__main__":
    unittest.main()
