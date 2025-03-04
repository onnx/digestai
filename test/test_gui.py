# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# pylint: disable=no-name-in-module
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QEventLoop, QTimer, Signal
from PySide6.QtWidgets import QApplication

from huggingface_hub.hf_api import ModelInfo
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
        cls.app.setQuitOnLastWindowClosed(True)  # Ensure proper cleanup
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if isinstance(cls.app, QApplication):
            cls.app.processEvents()
            cls.app.closeAllWindows()
            cls.app.quit()  # Explicitly quit the application
            cls.app = None
        return super().tearDownClass()

    def setUp(self):
        self.digest_app = digest.main.DigestApp()
        if self.digest_app is None:
            self.fail("Failed to initialize DigestApp")
        self.digest_app.show()
        self.initial_tab_count = self.digest_app.ui.tabWidget.count()
        QApplication.processEvents()  # Process initial events
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        """Ensure proper cleanup of Qt resources"""
        if self.digest_app:
            # Close all windows first
            for window in QApplication.topLevelWindows():
                window.close()
                QApplication.processEvents()

            # Wait for any pending threads with a shorter timeout
            if hasattr(self.digest_app, "thread_pool"):
                self.digest_app.thread_pool.clear()  # Cancel any pending tasks
                self.digest_app.thread_pool.waitForDone(2000)  # 2 second timeout

            QApplication.processEvents()
            self.digest_app.close()
            self.digest_app = None
            QApplication.processEvents()

    def _wait_for_signal(self, signal: Signal, timeout_ms=THREAD_TIMEOUT):
        """Wait for a signal to be emitted, with a timeout."""
        loop = QEventLoop()
        signal_emitted = []

        def on_signal_emitted():
            signal_emitted.append(True)
            loop.quit()

        signal.connect(on_signal_emitted)
        QTimer.singleShot(timeout_ms, loop.quit)
        loop.exec()

        return bool(signal_emitted)

    def _mock_file_open(self, mock_dialog, filepath):
        """Helper to mock file open dialog and wait for load completion."""
        mock_dialog.return_value = (filepath, "")
        QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)

    def _verify_tab_added(self):
        """Verify that exactly one new tab was added"""
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
        """Test opening a valid ONNX file."""
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            self._mock_file_open(mock_dialog, self.ONNX_FILEPATH)
            # Wait for the signal *after* clicking the button
            self.assertTrue(
                self._wait_for_signal(self.digest_app.model_loaded),
                "Model load did not complete within timeout (test_open_valid_onnx)",
            )
            self._verify_tab_added()  # Verify tab *after* successful load
            self._close_current_tab()

    def test_open_valid_yaml(self):
        """Test opening a valid YAML report file."""
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            self._mock_file_open(mock_dialog, self.YAML_FILEPATH)
            self.assertTrue(
                self._wait_for_signal(self.digest_app.model_loaded),
                "Model load did not complete within timeout (test_open_valid_yaml)",
            )
            self._verify_tab_added()
            self._close_current_tab()

    def test_open_invalid_file(self):
        """Test opening an invalid file (no tab should be added)."""
        with patch("PySide6.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
            mock_dialog.return_value = ("invalid_file.txt", "")
            QTest.mouseClick(self.digest_app.ui.openFileBtn, Qt.MouseButton.LeftButton)
            # No need to wait for a signal here, as it won't be emitted
            QApplication.processEvents()  # Process events to update UI
            self.assertEqual(
                self.digest_app.ui.tabWidget.count(),
                self.initial_tab_count,
                "No new tab should be added for invalid file",
            )

    def test_save_reports(self):
        """Test saving reports after loading a model."""
        with patch(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName"
        ) as mock_open_dialog, patch(
            "PySide6.QtWidgets.QFileDialog.getExistingDirectory"
        ) as mock_save_dialog:

            with tempfile.TemporaryDirectory() as tmpdirname:
                mock_save_dialog.return_value = tmpdirname
                self._mock_file_open(mock_open_dialog, self.ONNX_FILEPATH)
                # Wait for the signal
                self.assertTrue(
                    self._wait_for_signal(self.digest_app.model_loaded),
                    "Model load did not complete within timeout (save reports)",
                )

                QApplication.processEvents()  # Ensure UI is updated

                self.assertTrue(
                    self.digest_app.ui.saveBtn.isEnabled(),
                    "Save button should be enabled after loading file",
                )
                QTest.mouseClick(self.digest_app.ui.saveBtn, Qt.MouseButton.LeftButton)
                QApplication.processEvents()

    def test_save_tables(self):
        """Test saving node tables."""
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

                # Wait for the signal
                self.assertTrue(
                    self._wait_for_signal(self.digest_app.model_loaded),
                    "Model load did not complete within timeout (save tables)",
                )
                QApplication.processEvents()

                self._save_nodes_list(output_file)
                self._close_current_tab()

    def _navigate_to_huggingface_tab(self):
        """Navigate to the Huggingface tab."""
        self.digest_app.ui.stackedWidget.setCurrentIndex(
            self.digest_app.Page.HUGGINGFACE
        )
        QApplication.processEvents()

    def _mock_huggingface_api(self):
        """Mock the Huggingface API calls."""
        mock_model = MagicMock(spec=ModelInfo)
        mock_model.id = "test/model"
        mock_models = [mock_model]

        # Mock the API calls
        list_models_patch = patch(
            "huggingface_hub.hf_api.list_models", return_value=mock_models
        )
        list_files_patch = patch(
            "huggingface_hub.hf_api.list_repo_files", return_value=["model.onnx"]
        )

        return list_models_patch, list_files_patch

    def test_huggingface_search(self):
        """Test searching for models on Huggingface."""
        self._navigate_to_huggingface_tab()

        list_models_patch, list_files_patch = self._mock_huggingface_api()
        with list_models_patch as mock_list_models, list_files_patch as mock_list_files:
            hf_page = self.digest_app.ui.stackedWidget.currentWidget()

            hf_page.ui.hf_search_text.setPlainText("test model")
            QTest.mouseClick(hf_page.ui.hf_search_btn, Qt.MouseButton.LeftButton)

            self.assertTrue(
                self._wait_for_signal(hf_page.search_thread.signals.completed),
                "Huggingface search did not complete within timeout",
            )

            mock_list_models.assert_called_once()
            mock_list_files.assert_called_once_with("test/model")

            model = hf_page.ui.hf_column_view.model()
            self.assertIsNotNone(model, "Model should be set after search")
            self.assertEqual(model.rowCount(), 1, "Expected one model in results")

    def test_huggingface_model_selection(self):
        """Test selecting a model from Huggingface search results."""
        self._navigate_to_huggingface_tab()

        list_models_patch, list_files_patch = self._mock_huggingface_api()
        with list_models_patch as _, list_files_patch as _:
            hf_page = self.digest_app.ui.stackedWidget.currentWidget()

            hf_page.ui.hf_search_text.setPlainText("test model")
            QTest.mouseClick(hf_page.ui.hf_search_btn, Qt.MouseButton.LeftButton)

            self.assertTrue(
                self._wait_for_signal(hf_page.search_thread.signals.completed),
                "Huggingface search did not complete within timeout",
            )

            model_view = hf_page.ui.hf_column_view
            parent_index = model_view.model().index(0, 0)
            model_view.setCurrentIndex(parent_index)

            self.assertFalse(
                hf_page.ui.open_onnx_btn.isEnabled(),
                "Download button should be disabled when parent item is selected",
            )

            child_index = model_view.model().index(0, 0, parent_index)
            model_view.setCurrentIndex(child_index)

            selection = model_view.selectionModel().selection()
            hf_page.on_column_view_selection_change(selection)

            self.assertTrue(
                hf_page.ui.open_onnx_btn.isEnabled(),
                "Download button should be enabled when ONNX file is selected",
            )

            self.assertEqual(
                hf_page.currently_selected_hf_onnx["repo_id"], "test/model"
            )
            self.assertEqual(
                hf_page.currently_selected_hf_onnx["onnx_file"], "model.onnx"
            )

    def test_huggingface_download(self):
        """Test downloading a model from Huggingface."""
        self._navigate_to_huggingface_tab()

        list_models_patch, list_files_patch = self._mock_huggingface_api()
        with list_models_patch as _, list_files_patch as _:
            hf_page = self.digest_app.ui.stackedWidget.currentWidget()

            hf_page.ui.hf_search_text.setPlainText("test model")
            QTest.mouseClick(hf_page.ui.hf_search_btn, Qt.MouseButton.LeftButton)

            self.assertTrue(
                self._wait_for_signal(hf_page.search_thread.signals.completed),
                "Huggingface search did not complete within timeout",
            )

            model_view = hf_page.ui.hf_column_view
            parent_index = model_view.model().index(0, 0)
            model_view.setCurrentIndex(parent_index)

            child_index = model_view.model().index(0, 0, parent_index)
            model_view.setCurrentIndex(child_index)

            selection = model_view.selectionModel().selection()
            hf_page.on_column_view_selection_change(selection)

            self.assertEqual(
                hf_page.currently_selected_hf_onnx["repo_id"], "test/model"
            )
            self.assertEqual(
                hf_page.currently_selected_hf_onnx["onnx_file"], "model.onnx"
            )

            with patch("digest.huggingface_page.hf_hub_download") as mock_download:
                mock_download.return_value = "/tmp/fake/path/model.onnx"

                self.assertTrue(
                    hf_page.ui.open_onnx_btn.isEnabled(),
                    "Download button should be enabled when ONNX file is selected",
                )

                QTest.mouseClick(hf_page.ui.open_onnx_btn, Qt.MouseButton.LeftButton)

                self.assertTrue(
                    self._wait_for_signal(hf_page.model_signal),
                    "Model signal did not emit.",
                )

                # Process events.
                QApplication.processEvents()

                mock_download.assert_called_once_with(
                    "test/model", filename="model.onnx", force_download=True
                )

    def _save_nodes_list(self, expected_output):
        """Helper to handle nodes list saving logic"""
        QTest.mouseClick(self.digest_app.ui.nodesListBtn, Qt.MouseButton.LeftButton)

        # Get the node window and verify it
        if self.digest_app.nodes_window:
            _, node_window = self.digest_app.nodes_window.popitem()
            node_summary = node_window.main_window.centralWidget()
            self.assertIsInstance(node_summary, NodeSummary)

            if isinstance(node_summary, NodeSummary):
                QTest.mouseClick(node_summary.ui.saveCsvBtn, Qt.MouseButton.LeftButton)
                self.assertTrue(
                    os.path.exists(expected_output),
                    f"Nodes csv file not found at {expected_output}",
                )
        else:
            self.fail("Node summary window did not appear within timeout.")

    def _print_debug_info(self):
        """Print debug information about the current UI state."""
        current_tab = self.digest_app.ui.tabWidget.currentWidget()
        print(f"Current tab: {current_tab}")
        print(f"Tab count: {self.digest_app.ui.tabWidget.count()}")
        print(f"Save button enabled: {self.digest_app.ui.saveBtn.isEnabled()}")


if __name__ == "__main__":
    unittest.main()
