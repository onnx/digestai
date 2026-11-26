# Copyright (c) ONNX Project Contributors
#
# SPDX-License-Identifier: Apache-2.0

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SimilarityAnalysisReport(QMainWindow):
    def __init__(self, image_path, most_similar_models):
        super().__init__()
        self.setWindowTitle("Similarity Analysis Report")
        self.setWindowIcon(QIcon(":/assets/images/digest_logo_500.jpg"))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        self.enlarged_image_label = QLabel()
        layout.addWidget(self.enlarged_image_label)
        self.image_path = image_path
        self.update_enlarged_image()

        text_frame = QFrame()
        text_frame.setMinimumWidth(500)
        text_frame.setMaximumWidth(550)
        text_layout = QVBoxLayout(text_frame)
        text_layout.setContentsMargins(20, 100, 100, 20)

        self.title_label = QLabel("Similarity Analysis Heatmap")
        title_font = QFont("DejaVu Sans", 20)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)
        text_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.description_textedit = QTextEdit()
        self.description_textedit.setReadOnly(True)
        self.description_textedit.setMinimumHeight(600)
        self.description_textedit.setHtml(
            f"""
            <p style="font-family: 'DejaVu Sans'; font-size: 12pt; color: white;
            text-align: justify;"><br>This analysis works by extracting ops and subgraphs from the
            target model and comparing it with all models in a database. Our database contains over
            1,900 LLMs, transformers, and computer vision (TIMM) models. <br><br>
            Operators and subgraphs shown in Yellow <span style="color: yellow; font-size: 20px">
            &#9632;</span> represent elements that strongly correlate with the target model, while
            operators and subgraphs shown in Purple <span style="color: purple; font-size: 20px;">
            &#9632;</span> represent elements that are weakly correlated.<br>
            <h2>The most similar models found were:</h2>
            <ul style="font-family: 'Courier New', Courier, monospace;">
                <li>{most_similar_models[0]}</li>
                <li>{most_similar_models[1]}</li>
                <li>{most_similar_models[2]}</li>
            </ul>
            </p>
            """
        )
        text_layout.addWidget(self.description_textedit)
        layout.addWidget(text_frame)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        text_layout.addItem(spacer)
        self.resizeEvent = lambda event: self.update_enlarged_image()

    def update_enlarged_image(self):
        pixmap = QPixmap(self.image_path)
        max_image_width = int(self.width() * 0.6)
        pixmap = pixmap.scaledToWidth(
            max_image_width, Qt.TransformationMode.SmoothTransformation
        )
        self.enlarged_image_label.setPixmap(pixmap)

    def contextMenuEvent(self, event):
        menu = QMenu()
        copy_action = menu.addAction("Copy Image")
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == copy_action:
            self.copy_chart_to_clipboard()

    def copy_chart_to_clipboard(self):
        pixmap = QPixmap(self.enlarged_image_label.grab())
        QApplication.clipboard().setPixmap(pixmap)
