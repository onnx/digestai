# Digest API Examples: Python Scripts for Model Analysis

This directory contains Python scripts that demonstrate how to use the Digest API for ingesting, modifying, and analyzing machine learning models.

## Getting Started

Make sure DigestAI has been installed (see main README.md).

## Analysis

* Analyzes a single model or multiple models in a directory.
* Generates reports on model summary, node lists, node type counts, and node shape counts.
* Usage:

```bash

# Single model
python analysis.py /path/to/model.onnx /path/to/output/directory

# Multiple models
python analysis.py /path/to/model/directory /path/to/output/directory

```

### Understanding the Reports

The script generates various text and csv reports that provide insights into your models:

* Model Summary: Overview of the model's architecture, parameters, and FLOPs.
* Node List: Detailed list of all nodes in the model.
* Node Type Counts: Statistics on the types of nodes present in the model.
* Node Shape Counts: Statistics on the shapes of nodes in the model.


### Copyright
Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.
