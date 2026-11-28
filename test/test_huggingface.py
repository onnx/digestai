# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: E402

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from huggingface_hub.utils import HfHubHTTPError

# Match the path setup performed by digest.main for generated Qt UI imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "digest"))

from digest.huggingface_page import HFSearchThread


class TestHFSearchThread(unittest.TestCase):
    def test_search_uses_supported_filter_and_handles_hub_errors(self):
        thread = HFSearchThread("onnx")
        model = SimpleNamespace(id="org/model")

        with patch(
            "digest.huggingface_page.hf_api.list_models",
            return_value=[model],
        ) as list_models, patch(
            "digest.huggingface_page.hf_api.list_repo_files",
            side_effect=HfHubHTTPError(
                "Request failed",
                response=SimpleNamespace(headers={}, request=None),
            ),
        ):
            thread.run()

        list_models.assert_called_once_with(
            search="onnx", filter="library:onnx"
        )

    def test_search_reports_top_level_hub_errors(self):
        thread = HFSearchThread("onnx")
        errors = []
        thread.signals.failed.connect(errors.append)

        with patch(
            "digest.huggingface_page.hf_api.list_models",
            side_effect=HfHubHTTPError(
                "Search failed",
                response=SimpleNamespace(headers={}, request=None),
            ),
        ):
            thread.run()

        self.assertEqual(len(errors), 1)
        self.assertIn("Search failed", errors[0])


if __name__ == "__main__":
    unittest.main()
