# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# pylint: disable=no-name-in-module
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QDeadlineTimer
from PySide6.QtWidgets import QApplication

import digest.main
from digest.node_summary import NodeSummary

ONNX_BASENAME = "resnet18"
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
ONNX_FILEPATH = os.path.normpath(os.path.join(TEST_DIR, f"{ONNX_BASENAME}.onnx"))


class DigestGuiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        self.digest_app = digest.main.DigestApp()
        self.digest_app.show()

    def tearDown(self):
        self.wait_all_threads()
        self.digest_app.close()

    def wait_all_threads(self):

        for thread in self.digest_app.model_nodes_stats_thread.values():
            thread.wait(deadline=QDeadlineTimer.Forever)

        for thread in self.digest_app.model_similarity_thread.values():
            thread.wait(deadline=QDeadlineTimer.Forever)

    def test_open_valid_onnx(self):
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            mock_dialog.return_value = (
                ONNX_FILEPATH,
                "",
            )

            QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)

            self.wait_all_threads()

            self.assertTrue(
                self.digest_app.ui.tabWidget.count() > 0
            )  # Check if a tab was added

    def test_open_invalid_file(self):
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            mock_dialog.return_value = ("invalid_file.txt", "")
            QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)
            self.wait_all_threads()
            self.assertEqual(self.digest_app.ui.tabWidget.count(), 0)

    def test_save_reports(self):
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName"
        ) as mock_open_dialog, patch(
            "PySide6.QtWidgets.QFileDialog.getExistingDirectory"
        ) as mock_save_dialog:

            mock_open_dialog.return_value = (ONNX_FILEPATH, "")
            with tempfile.TemporaryDirectory() as tmpdirname:
                mock_save_dialog.return_value = tmpdirname

                QTest.mouseClick(
                    self.digest_app.ui.openFileBtn,
                    Qt.MouseButton.LeftButton,
                )

                self.wait_all_threads()

                # This is a slight hack but the issue is that model similarity takes
                # a bit longer to complete and we must have it done before the save
                # button is enabled guaranteeing all the artifacts are saved.
                # wait_all_threads() above doesn't seem to work. The only thing that
                # does is just waiting 5 seconds.
                QTest.qWait(5000)

                QTest.mouseClick(self.digest_app.ui.saveBtn, Qt.MouseButton.LeftButton)

                mock_save_dialog.assert_called_once()

                result_basepath = os.path.join(tmpdirname, f"{ONNX_BASENAME}_reports")

                # Text report test
                txt_report_filepath = os.path.join(
                    result_basepath, f"{ONNX_BASENAME}_report.txt"
                )
                self.assertTrue(os.path.isfile(txt_report_filepath))

                # Nodes test
                nodes_csv_report_filepath = os.path.join(
                    result_basepath, f"{ONNX_BASENAME}_nodes.csv"
                )
                self.assertTrue(os.path.isfile(nodes_csv_report_filepath))

                # Histogram test
                histogram_filepath = os.path.join(
                    result_basepath, f"{ONNX_BASENAME}_histogram.png"
                )
                self.assertTrue(os.path.isfile(histogram_filepath))

                # Heatmap test
                heatmap_filepath = os.path.join(
                    result_basepath, f"{ONNX_BASENAME}_heatmap.png"
                )
                self.assertTrue(os.path.isfile(heatmap_filepath))

    def test_save_tables(self):
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName"
        ) as mock_open_dialog, patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName"
        ) as mock_save_dialog:

            mock_open_dialog.return_value = (ONNX_FILEPATH, "")
            with tempfile.TemporaryDirectory() as tmpdirname:
                mock_save_dialog.return_value = (
                    os.path.join(tmpdirname, f"{ONNX_BASENAME}_nodes.csv"),
                    "",
                )

                QTest.mouseClick(
                    self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton
                )

                self.wait_all_threads()

                QTest.mouseClick(
                    self.digest_app.ui.nodesListBtn, Qt.MouseButton.LeftButton
                )

                # We assume there is only model loaded
                _, node_window = self.digest_app.nodes_window.popitem()
                node_summary = node_window.main_window.centralWidget()

                self.assertIsInstance(node_summary, NodeSummary)
                if isinstance(node_summary, NodeSummary):
                    QTest.mouseClick(
                        node_summary.ui.saveCsvBtn, Qt.MouseButton.LeftButton
                    )

                    mock_save_dialog.assert_called_once()

                self.assertTrue(
                    os.path.exists(
                        os.path.join(tmpdirname, f"{ONNX_BASENAME}_nodes.csv")
                    ),
                    "Nodes csv file not found.",
                )


if __name__ == "__main__":
    unittest.main()
