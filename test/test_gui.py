# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# pylint: disable=no-name-in-module
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

import digest.main
from digest.node_summary import NodeSummary


class DigestGuiTest(unittest.TestCase):
    MODEL_BASENAME = "resnet18"
    TEST_DIR = os.path.abspath(os.path.dirname(__file__))
    ONNX_FILEPATH = os.path.normpath(os.path.join(TEST_DIR, f"{MODEL_BASENAME}.onnx"))
    YAML_FILEPATH = os.path.normpath(
        os.path.join(
            TEST_DIR, f"{MODEL_BASENAME}_reports", f"{MODEL_BASENAME}_report.yaml"
        )
    )
    THREAD_TIMEOUT = 10000  # milliseconds

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
        self.initial_tab_count = self.digest_app.ui.tabWidget.count()
        self.addCleanup(self.digest_app.close)

    def tearDown(self):
        self.digest_app.close()
        QApplication.processEvents()  # Ensure all pending events are processed
        self.digest_app = None
        super().tearDown()

    def wait_all_threads(self, timeout_ms=None) -> bool:
        """Wait for all tasks in the thread pool to complete."""
        timeout_ms = timeout_ms or self.THREAD_TIMEOUT
        QApplication.processEvents()  # Ensure pending events are processed
        return self.digest_app.thread_pool.waitForDone(timeout_ms)

    def _mock_file_open(self, mock_dialog, filepath):
        """Helper to mock file open dialog"""
        mock_dialog.return_value = (filepath, "")
        QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)
        self.assertTrue(self.wait_all_threads())

    def _verify_tab_added(self):
        """Verify that exactly one new tab was added"""
        # Process events to ensure UI updates
        QApplication.processEvents()
        self.assertEqual(
            self.digest_app.ui.tabWidget.count(),
            self.initial_tab_count + 1,
            "Expected one new tab to be added",
        )

    def _close_current_tab(self):
        """Close the most recently opened tab"""
        current_tab = self.digest_app.ui.tabWidget.count() - 1
        self.digest_app.closeTab(current_tab)

    def test_open_valid_onnx(self):
        """Test that opening a valid ONNX file creates a new tab in the UI."""
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            self._mock_file_open(mock_dialog, self.ONNX_FILEPATH)
            self._verify_tab_added()
            self._close_current_tab()

    def test_open_valid_yaml(self):
        """Test that opening a valid YAML report file creates a new tab in the UI."""
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            self._mock_file_open(mock_dialog, self.YAML_FILEPATH)
            self._verify_tab_added()
            self._close_current_tab()

    def test_open_invalid_file(self):
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            self._mock_file_open(mock_dialog, "invalid_file.txt")
            self.assertEqual(
                self.digest_app.ui.tabWidget.count(),
                self.initial_tab_count,
                "No new tab should be added for invalid file",
            )

    def test_save_reports(self):
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName"
        ) as mock_open_dialog, patch(
            "PySide6.QtWidgets.QFileDialog.getExistingDirectory"
        ) as mock_save_dialog:

            with tempfile.TemporaryDirectory() as tmpdirname:
                mock_save_dialog.return_value = tmpdirname
                self._mock_file_open(mock_open_dialog, self.ONNX_FILEPATH)

                # Process any pending events and wait for threads
                QApplication.processEvents()

                self.assertTrue(
                    self.wait_all_threads(),
                    "Background tasks did not complete within the specified timeout",
                )

                # Process events again after threads complete
                QApplication.processEvents()

                # Add debug information
                self._print_debug_info()

                self.assertTrue(
                    self.digest_app.ui.saveBtn.isEnabled(),
                    "Save button should be enabled after loading file",
                )

    def test_save_tables(self):
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName"
        ) as mock_open_dialog, patch(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName"
        ) as mock_save_dialog:

            with tempfile.TemporaryDirectory() as tmpdirname:
                output_file = os.path.join(
                    tmpdirname, f"{self.MODEL_BASENAME}_nodes.csv"
                )
                mock_save_dialog.return_value = (output_file, "")

                self._mock_file_open(mock_open_dialog, self.ONNX_FILEPATH)

                # Process events and wait for threads before accessing nodes window
                QApplication.processEvents()
                self.assertTrue(
                    self.wait_all_threads(), "Threads did not complete in time"
                )

                self._save_nodes_list(output_file)
                self._close_current_tab()

    def _save_nodes_list(self, expected_output):
        """Helper to handle nodes list saving logic"""
        QTest.mouseClick(self.digest_app.ui.nodesListBtn, Qt.MouseButton.LeftButton)

        # Get the node window and verify it
        _, node_window = self.digest_app.nodes_window.popitem()
        node_summary = node_window.main_window.centralWidget()
        self.assertIsInstance(node_summary, NodeSummary)

        if isinstance(node_summary, NodeSummary):
            QTest.mouseClick(node_summary.ui.saveCsvBtn, Qt.MouseButton.LeftButton)
            self.assertTrue(
                os.path.exists(expected_output),
                f"Nodes csv file not found at {expected_output}",
            )

    def _print_debug_info(self):
        """Print debug information about the current UI state."""
        current_tab = self.digest_app.ui.tabWidget.currentWidget()
        print(f"Current tab: {current_tab}")
        print(f"Tab count: {self.digest_app.ui.tabWidget.count()}")
        print(f"Save button enabled: {self.digest_app.ui.saveBtn.isEnabled()}")


if __name__ == "__main__":
    unittest.main()
