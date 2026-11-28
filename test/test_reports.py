# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

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

            lines1 = [line.rstrip("\n") for line in f1]
            lines2 = [line.rstrip("\n") for line in f2]
            self.assertEqual(
                len(lines1),
                len(lines2),
                msg=f"Different line counts: {len(lines1)} vs {len(lines2)}",
            )
            self.assertEqual(lines1, lines2)

    def compare_csv_files(self, file1, file2, skip_lines=0):
        with open(file1, "r", encoding="utf-8") as f1, open(
            file2, "r", encoding="utf-8"
        ) as f2:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)

            for _ in range(skip_lines):  # Skip the specified number of lines
                next(reader1)
                next(reader2)

            rows1 = list(reader1)
            rows2 = list(reader2)
            self.assertEqual(
                len(rows1),
                len(rows2),
                msg=f"Different row counts: {len(rows1)} vs {len(rows2)}",
            )
            self.assertEqual(rows1, rows2)

    def test_against_example_reports(self):
        model_proto = onnx_utils.load_onnx(TEST_ONNX, load_external_data=False)
        model_name = os.path.splitext(os.path.basename(TEST_ONNX))[0]
        opt_model, _ = onnx_utils.optimize_onnx_model(model_proto)
        digest_model = DigestOnnxModel(
            opt_model,
            onnx_filepath=TEST_ONNX,
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
                        # import_list is excluded because the opset domains that
                        # onnxruntime's optimizer stamps into the optimized model
                        # vary across onnxruntime versions.
                        skip_keys=[
                            "report_date",
                            "model_file",
                            "digest_version",
                            "import_list",
                        ],
                    )
                )

            # Save CSV containing node-level information
            nodes_filepath = os.path.join(tmpdir, f"{model_name}_nodes.csv")
            digest_model.save_nodes_csv_report(nodes_filepath)
            with self.subTest("Testing nodes csv file"):
                self.compare_csv_files(TEST_NODES_CSV_REPORT, nodes_filepath)


if __name__ == "__main__":
    unittest.main()
