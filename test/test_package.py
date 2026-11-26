# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

import subprocess
import sys
import shutil
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]


def test_wheel_contains_runtime_data(tmp_path):
    project_copy = tmp_path / "project"
    project_copy.mkdir()
    for filename in ("pyproject.toml", "README.md", "LICENSE.txt"):
        shutil.copy2(REPOSITORY_ROOT / filename, project_copy / filename)
    shutil.copytree(REPOSITORY_ROOT / "src", project_copy / "src")

    wheel_directory = tmp_path / "wheel"
    wheel_directory.mkdir()
    subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from setuptools.build_meta import build_wheel; "
                "import sys; build_wheel(sys.argv[1])"
            ),
            str(wheel_directory),
        ],
        cwd=project_copy,
        check=True,
    )

    wheels = list(wheel_directory.glob("digestai-*.whl"))
    assert len(wheels) == 1

    with zipfile.ZipFile(wheels[0]) as wheel:
        packaged_files = set(wheel.namelist())

    assert {
        "digest/gui_config.yaml",
        "digest/styles/darkstyle.qss",
        "digest/subgraph_analysis/database.zip",
    } <= packaged_files
