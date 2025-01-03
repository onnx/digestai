# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

import os
from collections import OrderedDict
from typing import List, Tuple, Optional, Union
import inspect
import onnx
import torch
from digest.model_class.digest_onnx_model import DigestOnnxModel
from digest.model_class.digest_model import (
    DigestModel,
    SupportedModelTypes,
)


class DigestPyTorchModel(DigestModel):
    """The idea of this class is to first support PyTorch models by converting them to ONNX
    Eventually, we will want to support a PyTorch specific interface that has a custom GUI.
    To facilitate this process, it makes the most sense to use this class as helper class
    to convert the PyTorch model to ONNX and store the ONNX info in a member DigestOnnxModel
    object. We can also store various PyTorch specific details in this class as well.
    """

    def __init__(
        self,
        pytorch_file_path: str = "",
        model_name: str = "",
    ) -> None:
        super().__init__(pytorch_file_path, model_name, SupportedModelTypes.PYTORCH)

        assert os.path.exists(
            pytorch_file_path
        ), f"PyTorch file {pytorch_file_path} does not exist."

        # Default opset value
        self.opset = 17

        # Input dictionary to contain the names and shapes
        # required for exporting the ONNX model
        self.input_tensor_info: OrderedDict[
            str, Tuple[torch.dtype, List[Union[str, int]]]
        ] = OrderedDict()

        self.pytorch_model = torch.load(pytorch_file_path)

        # Data needed for exporting to ONNX
        self.do_constant_folding = True
        self.export_params = True

        self.onnx_file_path: Optional[str] = None

        self.digest_onnx_model: Optional[DigestOnnxModel] = None

    def parse_model_nodes(self) -> None:
        """This will be done in the DigestOnnxModel"""

    def save_yaml_report(self, file_path: str) -> None:
        """This will be done in the DigestOnnxModel"""

    def save_text_report(self, file_path: str) -> None:
        """This will be done in the DigestOnnxModel"""

    def generate_random_tensor(self, dtype: torch.dtype, shape: List[Union[str, int]]):
        static_shape = [dim if isinstance(dim, int) else 1 for dim in shape]
        if dtype in (torch.float16, torch.float32, torch.float64):
            return torch.rand(static_shape, dtype=dtype)
        else:
            return torch.randint(0, 100, static_shape, dtype=dtype)

    def export_to_onnx(self, output_onnx_path: str) -> Union[onnx.ModelProto, None]:

        dummy_input_names: List[str] = list(self.input_tensor_info.keys())
        dummy_inputs: List[torch.Tensor] = []

        for dtype, shape in self.input_tensor_info.values():
            dummy_inputs.append(self.generate_random_tensor(dtype, shape))

        dynamic_axes = {
            name: {i: dim for i, dim in enumerate(shape) if isinstance(dim, str)}
            for name, (_, shape) in self.input_tensor_info.items()
        }

        try:
            torch.onnx.export(
                self.pytorch_model,
                tuple(dummy_inputs),
                output_onnx_path,
                input_names=dummy_input_names,
                do_constant_folding=self.do_constant_folding,
                export_params=self.export_params,
                opset_version=self.opset,
                dynamic_axes=dynamic_axes,
                verbose=False,
            )

            self.onnx_file_path = output_onnx_path

            return onnx.load(output_onnx_path)

        except (ValueError, TypeError, RuntimeError) as err:
            print(f"Failed to export ONNX: {err}")
            raise


def get_model_fwd_parameters(torch_file_path):
    torch_model = torch.load(torch_file_path)
    return inspect.signature(torch_model.forward).parameters
