import os


def load_onnx(filepath: str):

    # Ensure the filepath follows a standard formatting:
    filepath = os.path.normpath(filepath)

    if not os.path.exists(filepath):
        return

    # Before opening the file, check to see if it is already opened.
    for index in range(self.ui.tabWidget.count()):
        widget = self.ui.tabWidget.widget(index)
        if isinstance(widget, modelSummary) and filepath == widget.file:
            self.ui.tabWidget.setCurrentIndex(index)
            return

    self.load_progress = ProgressDialog("Loading & Optimizing ONNX Model...", 3, self)
    self.load_progress.step()

    self.load_progress.setLabelText(
        "Creating a Digest model. Please be patient as this might take a minute."
    )

    basename = os.path.splitext(os.path.basename(filepath))
    model_name = basename[0]

    # Load the digest onnx model on a separate thread
    digest_model_worker = LoadDigestOnnxModelWorker(
        model_name=model_name, model_file_path=filepath
    )

    digest_model_worker.signals.completed.connect(self.post_load)

    self.thread_pool.start(digest_model_worker)


def load_report(filepath: str):

    # Ensure the filepath follows a standard formatting:
    filepath = os.path.normpath(filepath)

    if not os.path.exists(filepath):
        return

    # Every time a report is loaded we should emulate a model summary button click
    self.summary_clicked()

    # Before opening the file, check to see if it is already opened.
    for index in range(self.ui.tabWidget.count()):
        widget = self.ui.tabWidget.widget(index)
        if isinstance(widget, modelSummary) and filepath == widget.file:
            self.ui.tabWidget.setCurrentIndex(index)
            return

    try:

        progress = ProgressDialog("Loading Digest Report File...", 2, self)
        QApplication.processEvents()  # Process pending events

        digest_model = DigestReportModel(filepath)

        if not digest_model.is_valid:
            progress.close()
            invalid_yaml_dialog = StatusDialog(
                title="Warning",
                status_message=f"YAML file {filepath} is not a valid digest report",
            )
            invalid_yaml_dialog.show()

            return

        model_id = digest_model.unique_id

        # There is no sense in offering to save the report
        self.stats_save_button_flag[model_id] = False
        self.similarity_save_button_flag[model_id] = False

        self.digest_models[model_id] = digest_model

        model_summary = modelSummary(digest_model)

        self.ui.tabWidget.addTab(model_summary, "")
        model_summary.ui.flops.setText("Loading...")

        # Hide some of the components
        model_summary.ui.similarityCorrelation.hide()
        model_summary.ui.similarityCorrelationStatic.hide()

        model_summary.file = filepath
        model_summary.setObjectName(digest_model.model_name)
        model_summary.ui.modelName.setText(digest_model.model_name)
        model_summary.ui.modelFilename.setText(filepath)
        model_summary.ui.generatedDate.setText(datetime.now().strftime("%B %d, %Y"))

        model_summary.ui.parameters.setText(format(digest_model.parameters, ","))

        node_type_counts = digest_model.node_type_counts
        if len(node_type_counts) < 15:
            bar_spacing = 40
        else:
            bar_spacing = 20

        model_summary.ui.opHistogramChart.bar_spacing = bar_spacing
        model_summary.ui.opHistogramChart.set_data(node_type_counts)
        model_summary.ui.nodes.setText(str(sum(node_type_counts.values())))

        progress.step()
        progress.setLabelText("Gathering Model Inputs and Outputs")

        # Inputs Table
        model_summary.ui.inputsTable.setRowCount(
            len(self.digest_models[model_id].model_inputs)
        )

        for row_idx, (input_name, input_info) in enumerate(
            self.digest_models[model_id].model_inputs.items()
        ):
            model_summary.ui.inputsTable.setItem(
                row_idx, 0, QTableWidgetItem(input_name)
            )
            model_summary.ui.inputsTable.setItem(
                row_idx, 1, QTableWidgetItem(str(input_info.shape))
            )
            model_summary.ui.inputsTable.setItem(
                row_idx, 2, QTableWidgetItem(str(input_info.dtype))
            )
            model_summary.ui.inputsTable.setItem(
                row_idx, 3, QTableWidgetItem(str(input_info.size_kbytes))
            )

        model_summary.ui.inputsTable.resizeColumnsToContents()
        model_summary.ui.inputsTable.resizeRowsToContents()

        # Outputs Table
        model_summary.ui.outputsTable.setRowCount(
            len(self.digest_models[model_id].model_outputs)
        )
        for row_idx, (output_name, output_info) in enumerate(
            self.digest_models[model_id].model_outputs.items()
        ):
            model_summary.ui.outputsTable.setItem(
                row_idx, 0, QTableWidgetItem(output_name)
            )
            model_summary.ui.outputsTable.setItem(
                row_idx, 1, QTableWidgetItem(str(output_info.shape))
            )
            model_summary.ui.outputsTable.setItem(
                row_idx, 2, QTableWidgetItem(str(output_info.dtype))
            )
            model_summary.ui.outputsTable.setItem(
                row_idx, 3, QTableWidgetItem(str(output_info.size_kbytes))
            )

        model_summary.ui.outputsTable.resizeColumnsToContents()
        model_summary.ui.outputsTable.resizeRowsToContents()

        progress.step()
        progress.setLabelText("Gathering Model Proto Data")

        # ModelProto Info
        model_summary.ui.modelProtoTable.setItem(
            0, 1, QTableWidgetItem(str(digest_model.model_data["model_version"]))
        )

        model_summary.ui.modelProtoTable.setItem(
            1, 1, QTableWidgetItem(str(digest_model.model_data["graph_name"]))
        )

        producer_txt = (
            f"{digest_model.model_data['producer_name']} "
            f"{digest_model.model_data['producer_version']}"
        )
        model_summary.ui.modelProtoTable.setItem(2, 1, QTableWidgetItem(producer_txt))

        model_summary.ui.modelProtoTable.setItem(
            3, 1, QTableWidgetItem(str(digest_model.model_data["ir_version"]))
        )

        for domain, version in digest_model.model_data["import_list"].items():
            row_idx = model_summary.ui.importsTable.rowCount()
            model_summary.ui.importsTable.insertRow(row_idx)
            if domain == "" or domain == "ai.onnx":
                model_summary.ui.opsetVersion.setText(str(version))
                domain = "ai.onnx"

            model_summary.ui.importsTable.setItem(
                row_idx, 0, QTableWidgetItem(str(domain))
            )
            model_summary.ui.importsTable.setItem(
                row_idx, 1, QTableWidgetItem(str(version))
            )
            row_idx += 1

        progress.step()
        progress.setLabelText("Wrapping Up Model Analysis")

        model_summary.ui.importsTable.resizeColumnsToContents()
        model_summary.ui.modelProtoTable.resizeColumnsToContents()
        model_summary.setObjectName(digest_model.model_name)
        new_tab_idx = self.ui.tabWidget.count() - 1
        self.ui.tabWidget.setTabText(new_tab_idx, "".join(digest_model.model_name))
        self.ui.tabWidget.setCurrentIndex(new_tab_idx)
        self.ui.stackedWidget.setCurrentIndex(self.Page.SUMMARY)
        self.ui.singleModelWidget.show()
        progress.step()

        # self.update_cards(digest_model.unique_id)

        movie = QMovie(":/assets/gifs/load.gif")
        model_summary.ui.similarityImg.setMovie(movie)
        movie.start()

        self.update_similarity_widget(
            completed_successfully=bool(digest_model.similarity_heatmap_path),
            model_id=digest_model.unique_id,
            most_similar="",
            png_filepath=digest_model.similarity_heatmap_path,
        )

        progress.close()

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")


def load_model(file_path: str):

    # Ensure the filepath follows a standard formatting:
    file_path = os.path.normpath(file_path)

    if not os.path.exists(file_path):
        return

    file_ext = os.path.splitext(file_path)[-1]

    if file_ext == ".onnx":
        self.load_onnx(file_path)
    elif file_ext == ".yaml":
        self.load_report(file_path)
    else:
        bad_ext_dialog = StatusDialog(
            f"Digest does not support files with the extension {file_ext}",
            parent=self,
        )
        bad_ext_dialog.show()
