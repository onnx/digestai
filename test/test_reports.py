# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import unittest
import tempfile
import csv
from unittest.mock import patch
from onnx import TensorProto, helper
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

    def analyze_graph(self, nodes, inputs, outputs, initializers=None):
        graph = helper.make_graph(
            nodes,
            "flop_test",
            inputs,
            outputs,
            initializer=initializers or [],
        )
        model = helper.make_model(
            graph,
            opset_imports=[helper.make_opsetid("", 13)],
        )
        with patch.object(
            onnx_utils, "optimize_onnx_model", return_value=(model, None)
        ):
            return DigestOnnxModel(model, model_name="flop_test", save_proto=False)

    def test_gemm_flops_handle_optional_and_broadcast_bias(self):
        x = helper.make_tensor_value_info("X", TensorProto.FLOAT, [2, 3])
        y = helper.make_tensor_value_info("Y", TensorProto.FLOAT, [2, 4])
        weight = helper.make_tensor("W", TensorProto.FLOAT, [3, 4], [0.0] * 12)

        without_bias = self.analyze_graph(
            [helper.make_node("Gemm", ["X", "W"], ["Y"], name="gemm")],
            [x],
            [y],
            [weight],
        )
        self.assertEqual(without_bias.node_data["gemm"].flops, 48)

        bias = helper.make_tensor("B", TensorProto.FLOAT, [4], [0.0] * 4)
        with_bias = self.analyze_graph(
            [helper.make_node("Gemm", ["X", "W", "B"], ["Y"], name="gemm")],
            [x],
            [y],
            [weight, bias],
        )
        self.assertEqual(with_bias.node_data["gemm"].flops, 56)

    def test_elementwise_flops_follow_broadcast_output(self):
        model = self.analyze_graph(
            [helper.make_node("Add", ["A", "B"], ["Y"], name="add")],
            [
                helper.make_tensor_value_info("A", TensorProto.FLOAT, [2, 3]),
                helper.make_tensor_value_info("B", TensorProto.FLOAT, [3]),
            ],
            [helper.make_tensor_value_info("Y", TensorProto.FLOAT, [2, 3])],
        )

        self.assertEqual(model.node_data["add"].flops, 6)

    def test_same_convolution_uses_ceiling_output_shape(self):
        weight = helper.make_tensor(
            "W", TensorProto.FLOAT, [4, 3, 3, 3], [0.0] * 108
        )
        model = self.analyze_graph(
            [
                helper.make_node(
                    "Conv",
                    ["X", "W"],
                    ["Y"],
                    name="conv",
                    auto_pad="SAME_UPPER",
                    strides=[2, 2],
                )
            ],
            [helper.make_tensor_value_info("X", TensorProto.FLOAT, [1, 3, 8, 8])],
            [helper.make_tensor_value_info("Y", TensorProto.FLOAT, [1, 4, 4, 4])],
            [weight],
        )

        self.assertEqual(model.node_data["conv"].flops, 3456)

    def test_conv_transpose_channels_and_bias(self):
        weight = helper.make_tensor(
            "W", TensorProto.FLOAT, [4, 3, 3, 3], [0.0] * 108
        )
        bias = helper.make_tensor("B", TensorProto.FLOAT, [3], [0.0] * 3)
        model = self.analyze_graph(
            [
                helper.make_node(
                    "ConvTranspose",
                    ["X", "W", "B"],
                    ["Y"],
                    name="conv_transpose",
                    strides=[2, 2],
                )
            ],
            [helper.make_tensor_value_info("X", TensorProto.FLOAT, [1, 4, 4, 4])],
            [helper.make_tensor_value_info("Y", TensorProto.FLOAT, [1, 3, 9, 9])],
            [weight, bias],
        )

        self.assertEqual(model.node_data["conv_transpose"].flops, 17739)

    def test_shared_initializer_is_counted_once(self):
        weight = helper.make_tensor("W", TensorProto.FLOAT, [3, 4], [0.0] * 12)
        model = self.analyze_graph(
            [
                helper.make_node("MatMul", ["X1", "W"], ["Y1"], name="matmul_1"),
                helper.make_node("MatMul", ["X2", "W"], ["Y2"], name="matmul_2"),
            ],
            [
                helper.make_tensor_value_info("X1", TensorProto.FLOAT, [2, 3]),
                helper.make_tensor_value_info("X2", TensorProto.FLOAT, [2, 3]),
            ],
            [
                helper.make_tensor_value_info("Y1", TensorProto.FLOAT, [2, 4]),
                helper.make_tensor_value_info("Y2", TensorProto.FLOAT, [2, 4]),
            ],
            [weight],
        )

        self.assertEqual(model.parameters, 12)

    def test_symbolic_output_dimensions_are_preserved(self):
        model = self.analyze_graph(
            [helper.make_node("Identity", ["X"], ["Y"], name="identity")],
            [helper.make_tensor_value_info("X", TensorProto.FLOAT, ["batch", 3])],
            [helper.make_tensor_value_info("Y", TensorProto.FLOAT, ["batch", 3])],
        )

        self.assertEqual(model.node_data["identity"].get_output(0).shape, ["batch", 3])

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
