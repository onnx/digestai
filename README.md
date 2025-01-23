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

DigestAI is a powerful model analysis tool that extracts insights from your models, enabling optimization and direct modification.

**Get started quickly!** Download the DigestAI executable directly from [link coming soon].

**Developers: Contribute to DigestAI** Follow the installation instruction below to get started.

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

1. Start the gui

    ```bash
    digest
    ```

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

1. Setup the environment

* Follow the steps in the previous section `Installation Instructions for Developers` to create the `digestai` conda environment
* With the `digestai` conda environment activated install pyinstaller:

  ```
  pip install pyinstaller
  ```

* Run the following command to create the executable:

  ```
  pyinstaller.exe main.spec
  ```

  `digest.exe` will be built to `dist/digest.exe`.

## Contributing (WIP)

We welcome contributions! If you'd like to get involved, please:

1. Choose an Issue or Create One: Take a look at our existing issues to find something you'd like to work on. If you have a new idea, please create a new issue to discuss it with the maintainers.

1. Fork or Branch and Create a Pull Request (PR): Fork the repository, make your changes, and submit a PR.

1. Run GUI Test Locally: Before submitting your PR, verify your changes pass the local GUI test. This test is currently not part of our CI workflow and must be run manually from the digestai root directory using:

```bash
pip install pytest 
pytest test/test_gui.py
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE.txt) file for details.

## Copyright

Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.
