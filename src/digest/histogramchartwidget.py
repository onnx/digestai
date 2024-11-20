# Copyright(C) 2024 Advanced Micro Devices, Inc. All rights reserved.

from collections import OrderedDict

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QApplication,
    QGraphicsSceneHoverEvent,
    QMenu,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QFont, QBrush
import pyqtgraph as pg


class PlotWidgetCustom(pg.PlotWidget):
    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            super().wheelEvent(event)  # Zoom with Control key
        else:
            QApplication.sendEvent(self.parent(), event)  # Scroll otherwise


# pylint: disable=abstract-method
class InteractiveBarItem(pg.BarGraphItem):
    def __init__(
        self,
        percentage: float,
        x0: float,
        y0: float,
        width: float,
        height: float,
        brush: QBrush,
        *args,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        **kwargs,
    ):
        super().__init__(
            x0=x0, y0=y0, width=width, height=height, brush=brush, *args, **kwargs
        )
        self.setAcceptHoverEvents(True)
        self.default_color = brush.color()
        self.hover_color = QColor(30, 160, 220)
        self.orientation = orientation

        angle = 0 if orientation == Qt.Orientation.Vertical else -90
        if percentage < 1.5:
            self.label = pg.TextItem(
                text="", anchor=(0.5, 0.5), color=(0, 0, 0), angle=angle
            )
        else:
            self.label = pg.TextItem(
                text=f"{percentage}%", anchor=(0.5, 0.5), color=(0, 0, 0), angle=angle
            )

        self.label_font = QFont("Arial", 8, QFont.Weight.Bold)
        self.label.setFont(self.label_font)
        self.label.setParentItem(self)
        self.label.setVisible(False)

        y_center = y0 + height / 2
        x_center = x0 + width / 2
        self.label.setPos(x_center, y_center)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverEnterEvent(event)
        self.setOpts(brush=self.hover_color)
        self.label.setVisible(True)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverLeaveEvent(event)
        self.setOpts(brush=self.default_color)
        self.label.setVisible(False)


class HistogramChartWidget(QWidget):
    def __init__(self, *args, **kwargs):
        """
        bar_spacing refers to the offset spacing between bars. A larger
        spacing typically results in larger bars which has better
        aesthetics for histograms with fewer items.
        """
        super(HistogramChartWidget, self).__init__(*args, **kwargs)

        self.plot_widget = PlotWidgetCustom()

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        view_box = self.plot_widget.getViewBox()
        view_box.setMouseEnabled(x=False, y=False)
        view_box.setMenuEnabled(False)

        self.bar_spacing = 25

    def copy_chart_to_clipboard(self):
        if self.plot_widget:
            pixmap = QPixmap(self.plot_widget.grab())
            QApplication.clipboard().setPixmap(pixmap)

    def contextMenuEvent(self, event):
        menu = QMenu()
        copy_action = menu.addAction("Copy Image")
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == copy_action:
            self.copy_chart_to_clipboard()

    def set_data(self, data: OrderedDict, title="Op Histogram"):
        self.plot_widget.setTitle(
            f"<span style='color:rgb(200,200,200); font-size: 14pt'>{title}</span>"
        )
        op_count = list(data.values())[::-1]
        op_names = list(data.keys())[::-1]
        y_positions = list(range(len(op_count)))
        total_count = sum(op_count)
        height = 0.6
        self.plot_widget.setFixedHeight(len(op_names) * self.bar_spacing)
        for count, y_pos in zip(op_count, y_positions):
            bar = InteractiveBarItem(
                percentage=round(100.0 * count / total_count),
                x0=0,
                y0=y_pos - height / 2,
                width=count,
                height=height,
                brush=pg.mkBrush(color=(80, 80, 80)),
                orientation=Qt.Orientation.Vertical,
            )
            self.plot_widget.addItem(bar)

        axis = self.plot_widget.getAxis("left")
        ticks = [[(i, f"{op_names[i]} ({op_count[i]})") for i in y_positions]]
        axis.setTicks(ticks)


class StackedHistogramWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(StackedHistogramWidget, self).__init__(*args, **kwargs)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setMaximumHeight(150)
        plot_item = self.plot_widget.getPlotItem()
        if plot_item:
            plot_item.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        view_box = self.plot_widget.getViewBox()

        view_box.setMouseEnabled(x=False, y=False)
        view_box.setMenuEnabled(False)

        self.bar_spacing = 25

    def set_data(self, data: OrderedDict, model_name, y_max, title="", set_ticks=False):

        title_color = "rgb(0,0,0)" if set_ticks else "rgb(200,200,200)"
        self.plot_widget.setLabel(
            "left",
            f"<span style='color:{title_color}; font-size: 10pt'>{model_name}</span>",
        )
        if title:
            self.plot_widget.setTitle(
                f"<span style='color:{title_color}; font-size: 14pt'>{title}</span>"
            )
        self.plot_widget.setYRange(0, y_max)
        op_count = list(data.values())[::-1]
        op_names = list(data.keys())[::-1]
        x_positions = list(range(len(op_count)))
        total_count = sum(op_count)
        width = 0.6
        self.plot_widget.setFixedWidth(len(op_names) * self.bar_spacing)
        for count, x_pos, tick in zip(op_count, x_positions, op_names):
            x0 = x_pos - width / 2
            y0 = 0
            if set_ticks:
                tick_label = pg.TextItem(
                    text=tick,
                    anchor=(0, 0.5),
                    color=(255, 255, 255),
                    angle=-90,
                )

                tick_font = QFont("Arial", 8, QFont.Weight.Bold)
                tick_label.setFont(tick_font)
                tick_label.setVisible(True)
                y_center = y_max
                x_center = x0 + width / 2
                tick_label.setPos(x_center, y_center)
                self.plot_widget.addItem(tick_label)

                # Hide elements without losing their location
                self.plot_widget.getAxis("bottom").setPen(color="k")
                self.plot_widget.getAxis("left").setPen(color="k")
                axis = self.plot_widget.getAxis("left")
                ticks = [[(i, "_" * (1 + len(str(y_max)))) for i in x_positions]]
                axis.setTicks(ticks)

            bar = InteractiveBarItem(
                percentage=round(100.0 * count / total_count),
                x0=x0,
                y0=y0,
                width=width,
                height=count,
                brush=pg.mkBrush(color=(80, 80, 80)),
            )
            self.plot_widget.addItem(bar)

        axis = self.plot_widget.getAxis("bottom")
        ticks = [[(i, "") for i in x_positions]]
        axis.setTicks(ticks)
