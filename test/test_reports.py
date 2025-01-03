# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import unittest
import tempfile
import csv
import utils.onnx_utils as onnx_utils
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.model_class.digest_report_model import compare_yaml_files

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ONNX = os.path.join(TEST_DIR, "resnet18.onnx")
TEST_SUMMARY_TEXT_REPORT = os.path.join(
    TEST_DIR, "resnet18_reports/resnet18_report.txt"
)
TEST_SUMMARY_YAML_REPORT = os.path.join(
    TEST_DIR, "resnet18_reports/resnet18_report.yaml"
)
TEST_NODES_CSV_REPORT = os.path.join(TEST_DIR, "resnet18_reports/resnet18_nodes.csv")


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
        model_proto = onnx_utils.load_onnx(TEST_ONNX, load_external_data=False)
        model_name = os.path.splitext(os.path.basename(TEST_ONNX))[0]
        opt_model, _ = onnx_utils.optimize_onnx_model(model_proto)
        digest_model = DigestOnnxModel(
            opt_model,
            onnx_file_path=TEST_ONNX,
            model_name=model_name,
            save_proto=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Model yaml report
            yaml_report_filepath = os.path.join(tmpdir, f"{model_name}_report.yaml")
            digest_model.save_yaml_report(yaml_report_filepath)
            with self.subTest("Testing report yaml file"):
                self.assertTrue(
                    compare_yaml_files(
                        TEST_SUMMARY_YAML_REPORT,
                        yaml_report_filepath,
                        skip_keys=["report_date", "model_file", "digest_version"],
                    )
                )

            # Save CSV containing node-level information
            nodes_filepath = os.path.join(tmpdir, f"{model_name}_nodes.csv")
            digest_model.save_nodes_csv_report(nodes_filepath)
            with self.subTest("Testing nodes csv file"):
                self.compare_csv_files(TEST_NODES_CSV_REPORT, nodes_filepath)


if __name__ == "__main__":
    unittest.main()
