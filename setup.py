# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

from setuptools import setup, find_packages

setup(
    name="digestai",
    version="1.1.2",
    description="Model analysis toolkit",
    author="Philip Colangelo, Daniel Holanda",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"digest": ["subgraph_analysis/database.zip"]},
    install_requires=[
        "pyside6 >= 6.7.0",
        "onnx < 1.16.2",
        "onnxruntime >= 1.17.0",
        "pyqtgraph >= 0.13.7",
        "huggingface_hub >= 0.23.0",
        "pandas",
        "matplotlib",
        "networkx",
        "prettytable",
        "numpy<2",
        "platformdirs>=4.2.2",
        "pyyaml>=6.0.1",
        "psutil>=6.0.0",
    ],
    classifiers=[],
    entry_points={"console_scripts": ["digest = digest.main:main"]},
    python_requires=">=3.9, <3.11",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
