<!--
Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: Apache-2.0
-->

<div align="center">

DigestAI
===========================

<h3>DigestAI is a powerful model analysis tool that extracts insights from your models, enabling optimization and direct modification.</h3>

[![python](https://img.shields.io/badge/python-3.10-blue)](https://github.com/onnx/digestai)
![version](https://img.shields.io/badge/release-1.0-green)
[![license](https://img.shields.io/badge/license-Apache2.0-blue)](https://github.com/onnx/digestai/blob/master/LICENSE)

![logo](src/digest/assets/images/banner.png)
---

<div align="left">


## Table of Contents
- [Key Features](#key-features)
- [Get Started](#getting-started)
  - [Installation Instructions for Developers](#installation-instructions-for-developers)
- [Digest AI User Guide](#digest-ai-user-guide)
  - [Opening and Analyzing a Model](#opening-and-analyzing-a-model)
  - [Node List View](#node-list-view)
  - [Saving and Reporting](#saving-and-reporting)
  - [Multi-Model Analysis](#multi-model-analysis)
  - [Hugging Face Module](#hugging-face-module)
  - [Handling Dynamic Input Shapes](#handling-dynamic-input-shapes)
  - [Digest API](#digest-api)
- [Digest AI Developer Guide](#digest-ai-developer-guide)
  - [GUI Development Using QT](#using-qt-designer-for-gui-development)
  - [Building a Windows exe](#building-exe-for-windows-deployment)
  - [Contributing](#contributing-wip)
- [License](#license)
- [Code of Conduct](#code-of-conduct)

# Key Features

- Single Model Analysis:
  - Analyze individual models to extract parameters, FLOPs, protobuf metadata, histograms, model similarity, and IO tensors.
  - Freeze dynamic input shapes to ensure consistent calculations and analysis.
- Multi-Model Analysis:
  - Compare high-level statistics of multiple models side by side.
  - Batch process single model reports for efficient analysis.
- Reporting and Export:
  - Save all extracted statistics into comprehensive reports and CSV files for easy sharing and collaboration.
  - Open and view shared reports directly within the GUI for seamless integration.

For more insights on Digest AI, see our announcement blog [here](https://www.amd.com/en/developer/resources/technical-articles/digest-ai-model-ingestion-and-analysis-tool.html).


# Getting Started

- **Get started quickly!** Download the DigestAI executable directly from [link coming soon].

- **Developers: Contribute to DigestAI** Follow the installation instruction below to get started.

## Installation Instructions for Developers

1. Create a Conda Environment (recommended):

    ```bash
    conda create -n digestai python=3.10
    conda activate digestai
    ```

1. Clone the repository:

    ```bash
    git clone https://github.com/onnx/digestai.git
    ```

1. Install Digest AI:

    ```bash
    pip install -e digestai
    ```

1. Start the GUI

    ```bash
    digest
    ```

# Digest AI User Guide

<img src="https://github.com/onnx/digestai/blob/main/img/digest.gif" width="800" alt="Digest AI Demo"/>

### Opening and Analyzing a Model

In Digest, you can open a model in 3 ways:

1. In the left sidebar, you can open a model by clicking on the “Open a local model” button.
1. You can use the keyboard shortcut CTRL+O, which will open a file explorer where you can select the model you would like to open.
1. Or you can simply drag and drop a model file directly onto the interface.

DigestAI also allows you to load a Digest report from a shared YAML file, enabling you to view the report directly in the GUI.

When you select a model file, Digest AI checks model integrity, prepares it for analysis, and extracts key data. After the analysis is complete, you will see a detailed summary of your model, including:

- **Basic Details:** Parameters and FLOPs (Floating Point Operations), which is the algorithmic number of floating-point operations required to run a single set of inputs through the model.
-	**Advanced Insights:** Operation histogram, parameter and FLOPs intensity per operation type, and a model similarity graph comparing your model to other popular models.
-	**Model Inputs and Outputs:** Detailed information about tensor names, shapes, data types, and sizes.

### Node List View

There is also a Node List button that opens a window displaying all nodes in the model in a table format, which you can then sort on the various columns.

### Saving and Reporting

Digest AI allows you to save the model analysis using the “Save Report” button found in the left menu.

When you click the save button, specify a folder to save the reports. The following is an example of the files saved:

-	**Heatmap:** a PNG image that shows the similarity of the model to other public models.
-	**Node CSV Report:** contains all the model’s nodes, parameters, FLOPs, attributes, and inputs and outputs.
-	**Report:** a text document summarizing the model analysis.
-	**Histogram:** a PNG image of the operation count.
-	**Node Type Counts CSV Report:** contains all the model’s nodes and their counts.

### Multi-Model Analysis

Digest AI also includes support for multi-model analysis. By clicking the “Multi-Model Analysis” button, you can select a folder containing multiple models.

This will load a new view where the left pane will list unique models, while the right pane will indicate duplicates.

### Hugging Face Module

Digest AI also includes a Hugging Face module that enables users to download ONNX models directly from the Hugging Face hub without leaving Digest AI. You can search for a model, select it, and click Open. Digest AI will download the model, analyze it, and take you to the summary page.

This feature is currently in Beta. To enable it:

- Navigate to the file `src\digest\gui_config.yaml`
- Change the `huggingface` module from `false` to `true`

### Handling Dynamic Input Shapes

Some models may have dynamic input shapes, which can affect certain calculations like FLOPs. If you encounter this, Digest AI will display a warning message. To freeze a model with dynamic shapes, scroll down to the “Input Tensor” information section and click the blue snowflake icon next to the table.

This will open a utility where you can specify static dimensions for the inputs, and you can then save the modified model with static shapes.

## Digest API

Digest AI includes an API for ingesting, modifying, and analyzing machine learning models. This includes the ability to perform the following:
-	Analyzes a single model or multiple models in a directory.
-	Generates reports on model summary, node lists, node type counts, and node shape counts.

The `analysis.py` script can be found in the `examples/` directory.

```python
# Single model
python analysis.py /path/to/model.onnx /path/to/output/directory

# Multiple models
python analysis.py /path/to/model/directory /path/to/output/directory
```

For more information on Digest API, see the [Digest API Guide](examples\README.md).

# Digest AI Developer Guide

## Using Qt Designer for GUI Development

Qt Designer offers a visual (WYSIWYG) approach to creating user interfaces. This project leverages Qt Designer to build and maintain the UI files located in `src/digest/ui`.

**Key File Types:**

* **`*.ui`:** Qt Designer files – open these directly in Qt Designer to visually edit your interface.
* **`*.py`:** Python UI files – generated automatically (compiled) from the `.ui` files. These are used by your application code.

The following steps are recommended because they are reproducible, however, there are several ways to configure and run your workflow, so feel free to follow your own script. Ensure you followed the Installation Instructions for Developers above.

**Workflow**

1. **Open Qt Designer:**
   * **Activate Conda Environment:**  Ensure your `digest` Conda environment is activated.
   * **Launch:** Run `pyside6-designer.exe` from your terminal.

2. **Work with UI Files:**
   * Open any existing UI file (`.ui`) from `src/digest/ui`.
   * Design your interface using the drag-and-drop tools and property editor.
   * Resource Files (Optional): If your UI uses custom icons, images, or stylesheets, please leverage the Qt resource file (`.qrc`). This makes it easier to manage and package resources with the application.
   * Please add any new `.ui` files to the `.pylintrc` file.

3. **Recompile UI Files (After Making Changes):**
   * From your terminal, navigate to the project's root directory.
   * Run: `python src/digest/compile_digest_gui.py`

## Building EXE for Windows Deployment

  - Setup the environment by following the steps [Installation Instructions for Developers](#installation-instructions-for-developers) to create the `digestai` conda environment
  - With the `digestai` conda environment activated install pyinstaller:
  
    ```bash
    pip install pyinstaller
    ```

* Run the following command to create the executable:

  ```bash
  pyinstaller.exe main.spec
  ```

* `digest.exe` will be built to `dist/digest.exe`.

## Contributing

We welcome contributions! If you'd like to get involved, please:

1. Choose an Issue or Create One: Take a look at our existing issues to find something you'd like to work on. If you have a new idea, please create a new issue to discuss it with the maintainers.

1. Fork or Branch and Create a Pull Request (PR): Fork the repository, make your changes, and submit a PR. Ensure your PR has a clear description of the changes and refers to any issues it addresses (if applicable).

1. Run GUI Test Locally: Before submitting your PR, verify your changes pass the local GUI test. This test is currently not part of our CI workflow and must be run manually from the digestai root directory using:

```bash
pip install pytest 
pytest test/test_gui.py
```

## Contact

To get in touch, please reach out to us at [digestai@amd.com](mailto:digestai@amd.com).

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE.txt) file for details.

## Code of Conduct
The ONNX code of conduct is described at [ONNX Code of Conduct](https://onnx.ai/codeofconduct.html).

## Copyright

Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
