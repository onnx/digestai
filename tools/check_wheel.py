# Copyright (c) ONNX Project Contributors
# SPDX-License-Identifier: Apache-2.0

"""Install a release wheel in a clean venv and exercise it outside the checkout."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import venv


def main():
    root = Path(__file__).resolve().parents[1]
    wheels = list(Path(sys.argv[1] if len(sys.argv) > 1 else "dist").resolve().glob("*.whl"))
    if len(wheels) != 1:
        raise ValueError(f"Expected exactly one release wheel, found {len(wheels)}")
    with tempfile.TemporaryDirectory(prefix="digestai-wheel-") as directory:
        work = Path(directory)
        environment = work / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        subprocess.run(
            [str(python), "-m", "pip", "install", str(wheels[0]), "pytest"],
            cwd=work, env=env, check=True, timeout=600,
        )
        subprocess.run([str(python), "-m", "pip", "check"], cwd=work, env=env, check=True)
        subprocess.run(
            [str(python), "-m", "digest.main", "--smoke-test"],
            cwd=work, env=env, check=True, timeout=60,
        )
        shutil.copytree(root / "test", work / "test", ignore=shutil.ignore_patterns("__pycache__"))
        subprocess.run(
            [str(python), "-m", "pytest", "test/test_gui.py", "test/test_reports.py", "-q"],
            cwd=work, env=env, check=True, timeout=180,
        )


if __name__ == "__main__":
    main()
