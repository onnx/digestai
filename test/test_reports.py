# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

"""Unit tests for Vitis ONNX Model Analyzer """

import os
import unittest
import tempfile
import csv
from utils.onnx_utils import DigestOnnxModel, load_onnx

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ONNX = os.path.join(TEST_DIR, "resnet18.onnx")
TEST_SUMMARY_TXT_REPORT = os.path.join(TEST_DIR, "resnet18_test_summary.txt")
TEST_NODES_CSV_REPORT = os.path.join(TEST_DIR, "resnet18_test_nodes.csv")


class TestDigestReports(unittest.TestCase):

    def compare_files_line_by_line(self, file1, file2, skip_lines=0):
        with open(file1, "r", encoding="utf-8") as f1, open(
            file2, "r", encoding="utf-8"
        ) as f2:
            for _ in range(skip_lines):
                next(f1)
                next(f2)

            for line1, line2 in zip(f1, f2):
                line1 = line1.rstrip("\n")
                line2 = line2.rstrip("\n")
                self.assertEqual(
                    line1, line2, msg=f"Difference in line: {line1} vs {line2}"
                )

    def compare_csv_files(self, file1, file2, skip_lines=0):
        with open(file1, "r", encoding="utf-8") as f1, open(
            file2, "r", encoding="utf-8"
        ) as f2:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)

            for _ in range(skip_lines):  # Skip the specified number of lines
                next(reader1)
                next(reader2)

            for row1, row2 in zip(reader1, reader2):
                self.assertEqual(row1, row2, msg=f"Difference in row: {row1} vs {row2}")

    def test_against_example_reports(self):
        model_proto = load_onnx(TEST_ONNX)
        model_name = os.path.splitext(os.path.basename(TEST_ONNX))[0]
        digest_model = DigestOnnxModel(
            model_proto, onnx_filepath=TEST_ONNX, model_name=model_name, save_proto=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Model summary text report
            summary_filepath = os.path.join(tmpdir, f"{model_name}_summary.txt")
            digest_model.save_txt_report(summary_filepath)

            with self.subTest("Testing summary text file"):
                self.compare_files_line_by_line(
                    TEST_SUMMARY_TXT_REPORT,
                    summary_filepath,
                    skip_lines=2,
                )

            # Save CSV containing node-level information
            nodes_filepath = os.path.join(tmpdir, f"{model_name}_nodes.csv")
            digest_model.save_nodes_csv_report(nodes_filepath)

            with self.subTest("Testing nodes csv file"):
                self.compare_csv_files(TEST_NODES_CSV_REPORT, nodes_filepath)
