# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
import unittest
import tempfile
import csv
from typing import List, Optional, Dict, Any
import yaml
import utils.onnx_utils as onnx_utils
from digest.model_class.digest_onnx_model import DigestOnnxModel

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

    def compare_yaml_files(
        self, file1: str, file2: str, skip_keys: Optional[List[str]] = None
    ) -> bool:
        """
        Compare two YAML files, ignoring specified keys.

        :param file1: Path to the first YAML file
        :param file2: Path to the second YAML file
        :param skip_keys: List of keys to ignore in the comparison
        :return: True if the files are equal (ignoring specified keys), False otherwise
        """

        def load_yaml(file_path: str) -> Dict[str, Any]:
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)

        def compare_dicts(
            dict1: Dict[str, Any], dict2: Dict[str, Any], path: str = ""
        ) -> List[str]:
            differences = []
            all_keys = set(dict1.keys()) | set(dict2.keys())

            for key in all_keys:
                if skip_keys and key in skip_keys:
                    continue

                current_path = f"{path}.{key}" if path else key

                if key not in dict1:
                    differences.append(
                        f"Key '{current_path}' is missing in the first file"
                    )
                elif key not in dict2:
                    differences.append(
                        f"Key '{current_path}' is missing in the second file"
                    )
                elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    differences.extend(
                        compare_dicts(dict1[key], dict2[key], current_path)
                    )
                elif dict1[key] != dict2[key]:
                    differences.append(
                        f"Value mismatch for key '{current_path}': {dict1[key]} != {dict2[key]}"
                    )

            return differences

        yaml1 = load_yaml(file1)
        yaml2 = load_yaml(file2)

        differences = compare_dicts(yaml1, yaml2)

        if differences:
            print("Differences found:")
            for diff in differences:
                print(f"- {diff}")
            return False
        else:
            print("No differences found.")
            return True

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
                    self.compare_yaml_files(
                        TEST_SUMMARY_YAML_REPORT,
                        yaml_report_filepath,
                        skip_keys=["report_date", "onnx_file"],
                    )
                )

            # Save CSV containing node-level information
            nodes_filepath = os.path.join(tmpdir, f"{model_name}_nodes.csv")
            digest_model.save_nodes_csv_report(nodes_filepath)
            with self.subTest("Testing nodes csv file"):
                self.compare_csv_files(TEST_NODES_CSV_REPORT, nodes_filepath)


if __name__ == "__main__":
    unittest.main()
