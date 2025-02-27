# Copyright(C) 2025 Advanced Micro Devices, Inc. All rights reserved.

import sys
import colorsys
from typing import Any, List, Optional

# pylint: disable=no-name-in-module
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PySide6.QtCore import Qt, QMargins
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenu


def generate_colors(num_colors, base_colors):
    colors = []
    base_color_count = len(base_colors)
    for i in range(num_colors):
        base_index = i % base_color_count
        base_color = QColor(base_colors[base_index])
        hue = base_color.hslHueF()
        saturation = base_color.hslSaturationF()
        lightness = base_color.lightnessF()

        # Create variations by adjusting lightness with a larger range
        l_variation = 0.2 * (i // base_color_count)  # Vary by 20% per cycle
        l_direction = (
            1 if (i // base_color_count) % 2 == 0 else -1
        )  # Alternate direction
        new_l = max(
            0.2, min(lightness + l_variation * l_direction, 0.8)
        )  # Limit to 20%-80%

        r, g, b = colorsys.hls_to_rgb(hue, new_l, saturation)
        colors.append(QColor.fromRgbF(r, g, b))
    return colors


class PieChartWidget(QWidget):
    # layout: QVBoxLayout

    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_colors = ["#4682B4", "#696969", "#6495ED"]
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.chart_view = None
        self.total_sum: Optional[int] = None

    def set_data(self, title: str, labels: List[str], data: List[Any]):

        series = QPieSeries()

        colors = generate_colors(len(data), self.base_colors)

        self.total_sum = sum(data)

        for i, value in enumerate(data):
            pie_slice = QPieSlice(labels[i], value)  # Set both label and value
            pie_slice.setBrush(QColor(colors[i]))

            # Percentage calculation and label formatting
            percentage = round(100 * value / self.total_sum, 1)
            label = f"{labels[i]} - {percentage}%"  # Include category
            pie_slice.setLabel(label)

            # Calculate the relative luminance of the slice's color
            slice_color = colors[i]
            r, g, b = slice_color.getRgbF()[:3]  # Extract r, g, b directly
            relative_luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

            # Choose a label color based on luminance for contrast
            if relative_luminance > 0.5:
                label_color = Qt.GlobalColor.black  # Dark text on light background
            else:
                label_color = Qt.GlobalColor.white  # Light text on dark background

            pie_slice.setLabelColor(label_color)

            # Label customization
            # pie_slice.setLabelColor(QColor("#DDDDDD"))  # Lighter label color
            if percentage >= 25:
                pie_slice.setLabelVisible(True)  # Show labels always
                # pie_slice.setLabelArmLengthFactor(0.2)
                pie_slice.setLabelPosition(
                    QPieSlice.LabelPosition.LabelInsideHorizontal
                )

            # Connect hover events (optional, for highlighting)
            pie_slice.hovered.connect(
                lambda state, pie_slice=pie_slice: self.highlightSlice(pie_slice, state)
            )

            series.append(pie_slice)

        # Create chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setTitleBrush(QColor(200, 200, 200))
        chart.setTitleFont(QFont("Arial", 14))  # , weight=QFont.Weight.Bold))

        chart.setBackgroundBrush(QColor("transparent"))  # Dark background

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        chart.legend().setFont(QFont("Arial", 10))  # Customize legend font
        chart.legend().setLabelColor(QColor("#DDDDDD"))
        chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)  # Add animation

        # Remove Chart Margins and Padding:
        chart.layout().setContentsMargins(0, 0, 0, 0)  # Remove layout margins
        chart.setMargins(QMargins(0, 0, 0, 0))  # Remove chart margins
        chart.setBackgroundRoundness(0)

        # Create chart view
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.layout.addWidget(self.chart_view)

        # Connect hover events to slots
        for pie_slice in series.slices():
            pie_slice.hovered.connect(
                lambda state, pie_slice=pie_slice: self.highlightSlice(pie_slice, state)
            )

    def highlightSlice(self, pie_slice: QPieSlice, state: bool):
        if state:
            pie_slice.setExploded(True)
            pie_slice.setPen(QPen(pie_slice.brush().color().lighter(130), 4))
            pie_slice.setLabelVisible(True)  # Show label on hover
        else:
            pie_slice.setExploded(False)
            pie_slice.setPen(QPen(pie_slice.brush().color(), 2))
            # Hide label when not hovering if percentage is less than 10
            if self.total_sum:
                percentage = round(100 * pie_slice.value() / self.total_sum, 1)
                if percentage < 25:
                    pie_slice.setLabelVisible(False)

    def contextMenuEvent(self, event):
        menu = QMenu()
        copy_action = menu.addAction("Copy Image")
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == copy_action:
            self.copy_chart_to_clipboard()

    def copy_chart_to_clipboard(self):
        if self.chart_view:
            pixmap = QPixmap(self.chart_view.grab())
            QApplication.clipboard().setPixmap(pixmap)


class MainWindow(QMainWindow):
    def __init__(self, labels, data):
        super().__init__()
        chart_view = PieChartWidget()
        chart_view.set_data("Pie Chart", labels, data)

        # Create a layout for the main window
        layout = QVBoxLayout()
        layout.addWidget(chart_view)  # Add the chart_view to the layout

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)  # Set the central widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chart_labels = ["A", "B", "C"]
    chart_data = [1, 2, 3]
    window = MainWindow(chart_labels, chart_data)
    window.show()
    window.resize(800, 600)
    sys.exit(app.exec())
