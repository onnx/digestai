# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modelsummary.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from clickablelabel import ClickableLabel
from histogramchartwidget import HistogramChartWidget
from piechartwidget import PieChartWidget
import resource_rc

class Ui_modelSummary(object):
    def setupUi(self, modelSummary):
        if not modelSummary.objectName():
            modelSummary.setObjectName(u"modelSummary")
        modelSummary.resize(1061, 837)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(modelSummary.sizePolicy().hasHeightForWidth())
        modelSummary.setSizePolicy(sizePolicy)
        modelSummary.setStyleSheet(u"background: rgb(20,20,20);")
        self.verticalLayout = QVBoxLayout(modelSummary)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.modelNameFrame = QFrame(modelSummary)
        self.modelNameFrame.setObjectName(u"modelNameFrame")
        self.modelNameFrame.setAutoFillBackground(False)
        self.modelNameFrame.setStyleSheet(u"background: rgb(0,0,0);\n"
"/*background: transparent;*/\n"
"border-top-left-radius: 10px;\n"
"border-top-right-radius: 10px;")
        self.modelNameFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.modelNameFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.modelNameFrame)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.modelName = QLabel(self.modelNameFrame)
        self.modelName.setObjectName(u"modelName")
        font = QFont()
        font.setBold(True)
        self.modelName.setFont(font)
        self.modelName.setStyleSheet(u"QLabel {\n"
"    font-size: 28px;\n"
"    font-weight: bold;\n"
"	margin-bottom: -5px;\n"
"}")
        self.modelName.setWordWrap(True)
        self.modelName.setMargin(1)
        self.modelName.setIndent(5)
        self.modelName.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_17.addWidget(self.modelName)

        self.modelFilename = QLabel(self.modelNameFrame)
        self.modelFilename.setObjectName(u"modelFilename")
        self.modelFilename.setStyleSheet(u"padding-left: 5px;")
        self.modelFilename.setMargin(0)

        self.verticalLayout_17.addWidget(self.modelFilename)

        self.generatedDate = QLabel(self.modelNameFrame)
        self.generatedDate.setObjectName(u"generatedDate")
        font1 = QFont()
        font1.setItalic(True)
        self.generatedDate.setFont(font1)
        self.generatedDate.setStyleSheet(u"padding-left: 5px;")
        self.generatedDate.setMargin(0)

        self.verticalLayout_17.addWidget(self.generatedDate)


        self.verticalLayout.addWidget(self.modelNameFrame)

        self.warningLabel = QLabel(modelSummary)
        self.warningLabel.setObjectName(u"warningLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.warningLabel.sizePolicy().hasHeightForWidth())
        self.warningLabel.setSizePolicy(sizePolicy1)
        self.warningLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 10px;\n"
"    background-color: #FFCC00; \n"
"    border: 1px solid #996600; \n"
"    color: #333333;\n"
"    font-weight: bold;\n"
"    border-radius: 0px;\n"
"}")
        self.warningLabel.setMargin(5)

        self.verticalLayout.addWidget(self.warningLabel)

        self.summaryPanesLayout = QHBoxLayout()
        self.summaryPanesLayout.setObjectName(u"summaryPanesLayout")
        self.scrollArea = QScrollArea(modelSummary)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.WinPanel)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -558, 991, 1443))
        self.scrollAreaWidgetContents.setStyleSheet(u"background-color: black;")
        self.verticalLayout_20 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.cardFrame = QFrame(self.scrollAreaWidgetContents)
        self.cardFrame.setObjectName(u"cardFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cardFrame.sizePolicy().hasHeightForWidth())
        self.cardFrame.setSizePolicy(sizePolicy2)
        self.cardFrame.setStyleSheet(u"background: transparent; /*rgb(40,40,40)*/")
        self.cardFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cardFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.cardFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 1)
        self.cardWidget = QWidget(self.cardFrame)
        self.cardWidget.setObjectName(u"cardWidget")
        sizePolicy2.setHeightForWidth(self.cardWidget.sizePolicy().hasHeightForWidth())
        self.cardWidget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_2 = QHBoxLayout(self.cardWidget)
        self.horizontalLayout_2.setSpacing(13)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 6, 25, 35)
        self.opsetFrame = QFrame(self.cardWidget)
        self.opsetFrame.setObjectName(u"opsetFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.opsetFrame.sizePolicy().hasHeightForWidth())
        self.opsetFrame.setSizePolicy(sizePolicy3)
        self.opsetFrame.setMinimumSize(QSize(220, 70))
        self.opsetFrame.setMaximumSize(QSize(16777215, 80))
        self.opsetFrame.setStyleSheet(u"QFrame {\n"
"   background: rgb(30,30,30);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"   background: rgb(35,35,35);\n"
"}")
        self.opsetFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.opsetFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.opsetFrame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, 6, -1)
        self.opsetLabel = QLabel(self.opsetFrame)
        self.opsetLabel.setObjectName(u"opsetLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.opsetLabel.sizePolicy().hasHeightForWidth())
        self.opsetLabel.setSizePolicy(sizePolicy4)
        self.opsetLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"	 color: rgb(204, 14, 31);\n"
"    background: transparent;\n"
"}")
        self.opsetLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.opsetLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_5.addWidget(self.opsetLabel)

        self.opsetVersion = QLabel(self.opsetFrame)
        self.opsetVersion.setObjectName(u"opsetVersion")
        sizePolicy4.setHeightForWidth(self.opsetVersion.sizePolicy().hasHeightForWidth())
        self.opsetVersion.setSizePolicy(sizePolicy4)
        self.opsetVersion.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"}")
        self.opsetVersion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.opsetVersion.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_5.addWidget(self.opsetVersion)


        self.horizontalLayout_2.addWidget(self.opsetFrame)

        self.nodesFrame = QFrame(self.cardWidget)
        self.nodesFrame.setObjectName(u"nodesFrame")
        sizePolicy3.setHeightForWidth(self.nodesFrame.sizePolicy().hasHeightForWidth())
        self.nodesFrame.setSizePolicy(sizePolicy3)
        self.nodesFrame.setMinimumSize(QSize(220, 70))
        self.nodesFrame.setMaximumSize(QSize(16777215, 80))
        self.nodesFrame.setStyleSheet(u"QFrame {\n"
"   background: rgb(30,30,30);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"   background: rgb(35,35,35);\n"
"}")
        self.nodesFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.nodesFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.nodesFrame)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 9, -1, -1)
        self.nodesLabel = QLabel(self.nodesFrame)
        self.nodesLabel.setObjectName(u"nodesLabel")
        sizePolicy4.setHeightForWidth(self.nodesLabel.sizePolicy().hasHeightForWidth())
        self.nodesLabel.setSizePolicy(sizePolicy4)
        self.nodesLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"	 color: rgb(204, 14, 31);\n"
"    background: transparent;\n"
"}")
        self.nodesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nodesLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_12.addWidget(self.nodesLabel)

        self.nodes = QLabel(self.nodesFrame)
        self.nodes.setObjectName(u"nodes")
        sizePolicy4.setHeightForWidth(self.nodes.sizePolicy().hasHeightForWidth())
        self.nodes.setSizePolicy(sizePolicy4)
        self.nodes.setMinimumSize(QSize(150, 32))
        self.nodes.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"}")
        self.nodes.setScaledContents(False)
        self.nodes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nodes.setWordWrap(True)
        self.nodes.setMargin(0)
        self.nodes.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_12.addWidget(self.nodes)


        self.horizontalLayout_2.addWidget(self.nodesFrame)

        self.paramFrame = QFrame(self.cardWidget)
        self.paramFrame.setObjectName(u"paramFrame")
        sizePolicy3.setHeightForWidth(self.paramFrame.sizePolicy().hasHeightForWidth())
        self.paramFrame.setSizePolicy(sizePolicy3)
        self.paramFrame.setMinimumSize(QSize(220, 70))
        self.paramFrame.setMaximumSize(QSize(16777215, 80))
        self.paramFrame.setStyleSheet(u"QFrame {\n"
"   background: rgb(30,30,30);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"   background: rgb(35,35,35);\n"
"}")
        self.paramFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.paramFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.paramFrame)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.parametersLabel = QLabel(self.paramFrame)
        self.parametersLabel.setObjectName(u"parametersLabel")
        sizePolicy4.setHeightForWidth(self.parametersLabel.sizePolicy().hasHeightForWidth())
        self.parametersLabel.setSizePolicy(sizePolicy4)
        self.parametersLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"	 color: rgb(204, 14, 31);\n"
"    background: transparent;\n"
"}")
        self.parametersLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parametersLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_9.addWidget(self.parametersLabel)

        self.parameters = QLabel(self.paramFrame)
        self.parameters.setObjectName(u"parameters")
        sizePolicy4.setHeightForWidth(self.parameters.sizePolicy().hasHeightForWidth())
        self.parameters.setSizePolicy(sizePolicy4)
        self.parameters.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"}")
        self.parameters.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parameters.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_9.addWidget(self.parameters)


        self.horizontalLayout_2.addWidget(self.paramFrame)

        self.flopsFrame = QFrame(self.cardWidget)
        self.flopsFrame.setObjectName(u"flopsFrame")
        sizePolicy3.setHeightForWidth(self.flopsFrame.sizePolicy().hasHeightForWidth())
        self.flopsFrame.setSizePolicy(sizePolicy3)
        self.flopsFrame.setMinimumSize(QSize(220, 70))
        self.flopsFrame.setMaximumSize(QSize(16777215, 80))
        self.flopsFrame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.flopsFrame.setStyleSheet(u"QFrame {\n"
"   background: rgb(30,30,30);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"   background: rgb(35,35,35);\n"
"}")
        self.flopsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.flopsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.flopsFrame)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.flopsLabel = QLabel(self.flopsFrame)
        self.flopsLabel.setObjectName(u"flopsLabel")
        sizePolicy4.setHeightForWidth(self.flopsLabel.sizePolicy().hasHeightForWidth())
        self.flopsLabel.setSizePolicy(sizePolicy4)
        self.flopsLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"	 color: rgb(204, 14, 31);\n"
"    background: transparent;\n"
"}")
        self.flopsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flopsLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_11.addWidget(self.flopsLabel)

        self.flops = QLabel(self.flopsFrame)
        self.flops.setObjectName(u"flops")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.flops.sizePolicy().hasHeightForWidth())
        self.flops.setSizePolicy(sizePolicy5)
        self.flops.setMinimumSize(QSize(200, 32))
        self.flops.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"}")
        self.flops.setScaledContents(False)
        self.flops.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flops.setWordWrap(True)
        self.flops.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_11.addWidget(self.flops)


        self.horizontalLayout_2.addWidget(self.flopsFrame)


        self.horizontalLayout.addWidget(self.cardWidget)


        self.verticalLayout_20.addWidget(self.cardFrame)

        self.chartsLayout = QVBoxLayout()
        self.chartsLayout.setObjectName(u"chartsLayout")
        self.firstRowChartsLayout = QHBoxLayout()
        self.firstRowChartsLayout.setObjectName(u"firstRowChartsLayout")
        self.firstRowChartsLayout.setContentsMargins(-1, 20, -1, -1)
        self.opHistogramChart = HistogramChartWidget(self.scrollAreaWidgetContents)
        self.opHistogramChart.setObjectName(u"opHistogramChart")
        sizePolicy1.setHeightForWidth(self.opHistogramChart.sizePolicy().hasHeightForWidth())
        self.opHistogramChart.setSizePolicy(sizePolicy1)
        self.opHistogramChart.setMinimumSize(QSize(500, 300))

        self.firstRowChartsLayout.addWidget(self.opHistogramChart)

        self.parametersPieChart = PieChartWidget(self.scrollAreaWidgetContents)
        self.parametersPieChart.setObjectName(u"parametersPieChart")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.parametersPieChart.sizePolicy().hasHeightForWidth())
        self.parametersPieChart.setSizePolicy(sizePolicy6)
        self.parametersPieChart.setMinimumSize(QSize(300, 500))

        self.firstRowChartsLayout.addWidget(self.parametersPieChart)


        self.chartsLayout.addLayout(self.firstRowChartsLayout)

        self.secondRowChartsLayout = QHBoxLayout()
        self.secondRowChartsLayout.setObjectName(u"secondRowChartsLayout")
        self.secondRowChartsLayout.setContentsMargins(-1, 20, -1, -1)
        self.similarityWidget = QWidget(self.scrollAreaWidgetContents)
        self.similarityWidget.setObjectName(u"similarityWidget")
        sizePolicy6.setHeightForWidth(self.similarityWidget.sizePolicy().hasHeightForWidth())
        self.similarityWidget.setSizePolicy(sizePolicy6)
        self.similarityWidget.setMinimumSize(QSize(300, 500))
        self.placeholderWidget = QVBoxLayout(self.similarityWidget)
        self.placeholderWidget.setObjectName(u"placeholderWidget")
        self.similarityImg = ClickableLabel(self.similarityWidget)
        self.similarityImg.setObjectName(u"similarityImg")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.similarityImg.sizePolicy().hasHeightForWidth())
        self.similarityImg.setSizePolicy(sizePolicy7)
        self.similarityImg.setMinimumSize(QSize(0, 0))
        self.similarityImg.setMaximumSize(QSize(16777215, 16777215))
        self.similarityImg.setScaledContents(False)
        self.similarityImg.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.placeholderWidget.addWidget(self.similarityImg)

        self.similarityCorrelationStatic = QLabel(self.similarityWidget)
        self.similarityCorrelationStatic.setObjectName(u"similarityCorrelationStatic")
        sizePolicy2.setHeightForWidth(self.similarityCorrelationStatic.sizePolicy().hasHeightForWidth())
        self.similarityCorrelationStatic.setSizePolicy(sizePolicy2)
        self.similarityCorrelationStatic.setFont(font)
        self.similarityCorrelationStatic.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.placeholderWidget.addWidget(self.similarityCorrelationStatic)

        self.similarityCorrelation = QLabel(self.similarityWidget)
        self.similarityCorrelation.setObjectName(u"similarityCorrelation")
        sizePolicy2.setHeightForWidth(self.similarityCorrelation.sizePolicy().hasHeightForWidth())
        self.similarityCorrelation.setSizePolicy(sizePolicy2)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.similarityCorrelation.setPalette(palette)
        self.similarityCorrelation.setFont(font)
        self.similarityCorrelation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.placeholderWidget.addWidget(self.similarityCorrelation)


        self.secondRowChartsLayout.addWidget(self.similarityWidget)

        self.flopsPieChart = PieChartWidget(self.scrollAreaWidgetContents)
        self.flopsPieChart.setObjectName(u"flopsPieChart")
        sizePolicy6.setHeightForWidth(self.flopsPieChart.sizePolicy().hasHeightForWidth())
        self.flopsPieChart.setSizePolicy(sizePolicy6)
        self.flopsPieChart.setMinimumSize(QSize(300, 500))

        self.secondRowChartsLayout.addWidget(self.flopsPieChart)


        self.chartsLayout.addLayout(self.secondRowChartsLayout)


        self.verticalLayout_20.addLayout(self.chartsLayout)

        self.thirdRowInputsLayout = QHBoxLayout()
        self.thirdRowInputsLayout.setObjectName(u"thirdRowInputsLayout")
        self.thirdRowInputsLayout.setContentsMargins(20, 30, -1, -1)
        self.inputsLayout = QVBoxLayout()
        self.inputsLayout.setObjectName(u"inputsLayout")
        self.inputsLabel = QLabel(self.scrollAreaWidgetContents)
        self.inputsLabel.setObjectName(u"inputsLabel")
        self.inputsLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"}")

        self.inputsLayout.addWidget(self.inputsLabel)

        self.inputsTable = QTableWidget(self.scrollAreaWidgetContents)
        if (self.inputsTable.columnCount() < 4):
            self.inputsTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.inputsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.inputsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.inputsTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.inputsTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.inputsTable.setObjectName(u"inputsTable")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.inputsTable.sizePolicy().hasHeightForWidth())
        self.inputsTable.setSizePolicy(sizePolicy8)
        self.inputsTable.setStyleSheet(u"QTableWidget {\n"
"    gridline-color: #353535; /* Grid lines */\n"
"    selection-background-color: #3949AB; /* Blue selection */\n"
"    border: none; /* Remove default border */\n"
"    padding: 5px; /* Add some padding */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    color: white; /* White text */\n"
"    padding: 5px;\n"
"    border-bottom: 1px solid #353535; /* Subtle divider between rows */\n"
"    border-left: 1px solid #353535;  /* Add left border to each cell */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #3949AB; /* Blue selection */\n"
"    color: white;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #333333; /* Header background */\n"
"    color: white;\n"
"    padding: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
"QHeaderView::section:checked {\n"
"    background-color: #3949AB; /* Blue when column is selected */\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background-color: #222222;\n"
"    width: 15px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    ba"
                        "ckground-color: #555555;\n"
"    border-radius: 5px;\n"
"}")
        self.inputsTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inputsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inputsTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.inputsTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.inputsTable.setShowGrid(True)
        self.inputsTable.setColumnCount(4)
        self.inputsTable.horizontalHeader().setVisible(True)
        self.inputsTable.verticalHeader().setVisible(False)
        self.inputsTable.verticalHeader().setHighlightSections(True)

        self.inputsLayout.addWidget(self.inputsTable)


        self.thirdRowInputsLayout.addLayout(self.inputsLayout)

        self.freezeButton = QPushButton(self.scrollAreaWidgetContents)
        self.freezeButton.setObjectName(u"freezeButton")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.freezeButton.sizePolicy().hasHeightForWidth())
        self.freezeButton.setSizePolicy(sizePolicy9)
        self.freezeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.freezeButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"    background-color: #056CF2;\n"
"	border: 1px solid rgba(60, 60, 60, 0.8);\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 30px;\n"
"	margin-left: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #0597F2;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #0554F2;\n"
"}\n"
"\n"
"")
        icon = QIcon()
        icon.addFile(u":/assets/icons/freeze.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.freezeButton.setIcon(icon)
        self.freezeButton.setIconSize(QSize(32, 32))

        self.thirdRowInputsLayout.addWidget(self.freezeButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.thirdRowInputsLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_20.addLayout(self.thirdRowInputsLayout)

        self.fourthRowOutputsLayout = QHBoxLayout()
        self.fourthRowOutputsLayout.setObjectName(u"fourthRowOutputsLayout")
        self.fourthRowOutputsLayout.setContentsMargins(20, 30, -1, -1)
        self.outputsLayout = QVBoxLayout()
        self.outputsLayout.setObjectName(u"outputsLayout")
        self.outputsLabel = QLabel(self.scrollAreaWidgetContents)
        self.outputsLabel.setObjectName(u"outputsLabel")
        self.outputsLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"}")

        self.outputsLayout.addWidget(self.outputsLabel)

        self.outputsTable = QTableWidget(self.scrollAreaWidgetContents)
        if (self.outputsTable.columnCount() < 4):
            self.outputsTable.setColumnCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.outputsTable.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.outputsTable.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.outputsTable.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.outputsTable.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        self.outputsTable.setObjectName(u"outputsTable")
        sizePolicy8.setHeightForWidth(self.outputsTable.sizePolicy().hasHeightForWidth())
        self.outputsTable.setSizePolicy(sizePolicy8)
        self.outputsTable.setStyleSheet(u"QTableWidget {\n"
"    gridline-color: #353535; /* Grid lines */\n"
"    selection-background-color: #3949AB; /* Blue selection */\n"
"    border: none; /* Remove default border */\n"
"    padding: 5px; /* Add some padding */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    color: white; /* White text */\n"
"    padding: 5px;\n"
"    border-bottom: 1px solid #353535; /* Subtle divider between rows */\n"
"    border-left: 1px solid #353535;  /* Add left border to each cell */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #3949AB; /* Blue selection */\n"
"    color: white;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #333333; /* Header background */\n"
"    color: white;\n"
"    padding: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
"QHeaderView::section:checked {\n"
"    background-color: #3949AB; /* Blue when column is selected */\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background-color: #222222;\n"
"    width: 15px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    ba"
                        "ckground-color: #555555;\n"
"    border-radius: 5px;\n"
"}")
        self.outputsTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.outputsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.outputsTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.outputsTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.outputsTable.setShowGrid(True)
        self.outputsTable.setColumnCount(4)
        self.outputsTable.horizontalHeader().setVisible(True)
        self.outputsTable.horizontalHeader().setStretchLastSection(False)
        self.outputsTable.verticalHeader().setVisible(False)
        self.outputsTable.verticalHeader().setHighlightSections(True)
        self.outputsTable.verticalHeader().setStretchLastSection(False)

        self.outputsLayout.addWidget(self.outputsTable)


        self.fourthRowOutputsLayout.addLayout(self.outputsLayout)


        self.verticalLayout_20.addLayout(self.fourthRowOutputsLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.summaryPanesLayout.addWidget(self.scrollArea)

        self.sidePaneFrame = QFrame(modelSummary)
        self.sidePaneFrame.setObjectName(u"sidePaneFrame")
        sizePolicy2.setHeightForWidth(self.sidePaneFrame.sizePolicy().hasHeightForWidth())
        self.sidePaneFrame.setSizePolicy(sizePolicy2)
        self.sidePaneFrame.setMinimumSize(QSize(0, 0))
        self.sidePaneFrame.setStyleSheet(u"QFrame {\n"
"   /*background: rgb(30,30,30);*/\n"
"    border-radius: 5px;\n"
"}")
        self.sidePaneFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidePaneFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.sidePaneFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.modelProtoLabel = QLabel(self.sidePaneFrame)
        self.modelProtoLabel.setObjectName(u"modelProtoLabel")
        self.modelProtoLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"	 color: rgb(204, 14, 31);\n"
"    background: transparent;\n"
"}")

        self.verticalLayout_3.addWidget(self.modelProtoLabel)

        self.modelProtoTable = QTableWidget(self.sidePaneFrame)
        if (self.modelProtoTable.columnCount() < 2):
            self.modelProtoTable.setColumnCount(2)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.modelProtoTable.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.modelProtoTable.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        if (self.modelProtoTable.rowCount() < 4):
            self.modelProtoTable.setRowCount(4)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.modelProtoTable.setVerticalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.modelProtoTable.setVerticalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.modelProtoTable.setVerticalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.modelProtoTable.setVerticalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled);
        self.modelProtoTable.setItem(0, 0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.modelProtoTable.setItem(0, 1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.modelProtoTable.setItem(1, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.modelProtoTable.setItem(1, 1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.modelProtoTable.setItem(2, 0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.modelProtoTable.setItem(2, 1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.modelProtoTable.setItem(3, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.modelProtoTable.setItem(3, 1, __qtablewidgetitem21)
        self.modelProtoTable.setObjectName(u"modelProtoTable")
        sizePolicy2.setHeightForWidth(self.modelProtoTable.sizePolicy().hasHeightForWidth())
        self.modelProtoTable.setSizePolicy(sizePolicy2)
        self.modelProtoTable.setMinimumSize(QSize(0, 0))
        self.modelProtoTable.setMaximumSize(QSize(16777215, 100))
        self.modelProtoTable.setStyleSheet(u"QTableWidget::item {\n"
"    color: white;\n"
"    padding: 5px;\n"
"    border-bottom: 0px; \n"
"    border-left: 0px;  \n"
"}\n"
"")
        self.modelProtoTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.modelProtoTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.modelProtoTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.modelProtoTable.setAutoScrollMargin(10)
        self.modelProtoTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.modelProtoTable.setDragDropOverwriteMode(False)
        self.modelProtoTable.setShowGrid(False)
        self.modelProtoTable.setCornerButtonEnabled(False)
        self.modelProtoTable.setRowCount(4)
        self.modelProtoTable.horizontalHeader().setVisible(False)
        self.modelProtoTable.horizontalHeader().setCascadingSectionResizes(False)
        self.modelProtoTable.horizontalHeader().setMinimumSectionSize(30)
        self.modelProtoTable.horizontalHeader().setDefaultSectionSize(115)
        self.modelProtoTable.verticalHeader().setVisible(False)
        self.modelProtoTable.verticalHeader().setCascadingSectionResizes(False)
        self.modelProtoTable.verticalHeader().setMinimumSectionSize(20)
        self.modelProtoTable.verticalHeader().setDefaultSectionSize(20)

        self.verticalLayout_3.addWidget(self.modelProtoTable)

        self.importsLabel = QLabel(self.sidePaneFrame)
        self.importsLabel.setObjectName(u"importsLabel")
        self.importsLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"	 color: rgb(204, 14, 31);\n"
"    background: transparent;\n"
"}")

        self.verticalLayout_3.addWidget(self.importsLabel)

        self.importsTable = QTableWidget(self.sidePaneFrame)
        if (self.importsTable.columnCount() < 2):
            self.importsTable.setColumnCount(2)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.importsTable.setHorizontalHeaderItem(0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.importsTable.setHorizontalHeaderItem(1, __qtablewidgetitem23)
        self.importsTable.setObjectName(u"importsTable")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.importsTable.sizePolicy().hasHeightForWidth())
        self.importsTable.setSizePolicy(sizePolicy10)
        self.importsTable.setStyleSheet(u"QTableWidget::item {\n"
"    color: white;\n"
"    padding: 5px;\n"
"    border-bottom: 0px; \n"
"    border-left: 0px;  \n"
"}\n"
"")
        self.importsTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.importsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.importsTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.importsTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.importsTable.setShowGrid(False)
        self.importsTable.horizontalHeader().setVisible(False)
        self.importsTable.verticalHeader().setVisible(False)
        self.importsTable.verticalHeader().setHighlightSections(True)

        self.verticalLayout_3.addWidget(self.importsTable)


        self.summaryPanesLayout.addWidget(self.sidePaneFrame)


        self.verticalLayout.addLayout(self.summaryPanesLayout)


        self.retranslateUi(modelSummary)

        QMetaObject.connectSlotsByName(modelSummary)
    # setupUi

    def retranslateUi(self, modelSummary):
        modelSummary.setWindowTitle(QCoreApplication.translate("modelSummary", u"Form", None))
        self.modelName.setText(QCoreApplication.translate("modelSummary", u"modelName", None))
        self.modelFilename.setText(QCoreApplication.translate("modelSummary", u"model_filename", None))
        self.generatedDate.setText(QCoreApplication.translate("modelSummary", u"date", None))
        self.warningLabel.setText(QCoreApplication.translate("modelSummary", u"<html><head/><body><p>This is a warning message that we can use for now to prompt the user.</p></body></html>", None))
        self.opsetLabel.setText(QCoreApplication.translate("modelSummary", u"Opset", None))
        self.opsetVersion.setText(QCoreApplication.translate("modelSummary", u"19", None))
        self.nodesLabel.setText(QCoreApplication.translate("modelSummary", u"Total Nodes", None))
        self.nodes.setText(QCoreApplication.translate("modelSummary", u"736", None))
        self.parametersLabel.setText(QCoreApplication.translate("modelSummary", u"Parameters", None))
        self.parameters.setText(QCoreApplication.translate("modelSummary", u"1,234,567,890", None))
        self.flopsLabel.setText(QCoreApplication.translate("modelSummary", u"FLOPs", None))
        self.flops.setText(QCoreApplication.translate("modelSummary", u"--", None))
        self.similarityImg.setText(QCoreApplication.translate("modelSummary", u"Loading...", None))
        self.similarityCorrelationStatic.setText(QCoreApplication.translate("modelSummary", u"This model most closely correlates with:", None))
        self.similarityCorrelation.setText(QCoreApplication.translate("modelSummary", u"Model 1, Model2, Model3.", None))
        self.inputsLabel.setText(QCoreApplication.translate("modelSummary", u"<html><head/><body><p><span style=\" font-size:12pt;\">Input Tensor(s) Information</span></p></body></html>", None))
        ___qtablewidgetitem = self.inputsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("modelSummary", u"Name", None));
        ___qtablewidgetitem1 = self.inputsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("modelSummary", u"Shape", None));
        ___qtablewidgetitem2 = self.inputsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("modelSummary", u"Dtype", None));
        ___qtablewidgetitem3 = self.inputsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("modelSummary", u"Tensor Size (kB)", None));
#if QT_CONFIG(tooltip)
        self.freezeButton.setToolTip(QCoreApplication.translate("modelSummary", u"Set static input dimensions", None))
#endif // QT_CONFIG(tooltip)
        self.freezeButton.setText("")
        self.outputsLabel.setText(QCoreApplication.translate("modelSummary", u"<html><head/><body><p><span style=\" font-size:12pt;\">Output Tensor(s) Information</span></p></body></html>", None))
        ___qtablewidgetitem4 = self.outputsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("modelSummary", u"Name", None));
        ___qtablewidgetitem5 = self.outputsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("modelSummary", u"Shape", None));
        ___qtablewidgetitem6 = self.outputsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("modelSummary", u"Dtype", None));
        ___qtablewidgetitem7 = self.outputsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("modelSummary", u"Tensor Size (kB)", None));
        self.modelProtoLabel.setText(QCoreApplication.translate("modelSummary", u"<html><head/><body><p><span style=\" font-size:12pt;\">Model Proto Info</span></p></body></html>", None))
        ___qtablewidgetitem8 = self.modelProtoTable.horizontalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("modelSummary", u"Key", None));
        ___qtablewidgetitem9 = self.modelProtoTable.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("modelSummary", u"Value", None));
        ___qtablewidgetitem10 = self.modelProtoTable.verticalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("modelSummary", u"row1", None));
        ___qtablewidgetitem11 = self.modelProtoTable.verticalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("modelSummary", u"row2", None));
        ___qtablewidgetitem12 = self.modelProtoTable.verticalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("modelSummary", u"row3", None));
        ___qtablewidgetitem13 = self.modelProtoTable.verticalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("modelSummary", u"row4", None));

        __sortingEnabled = self.modelProtoTable.isSortingEnabled()
        self.modelProtoTable.setSortingEnabled(False)
        ___qtablewidgetitem14 = self.modelProtoTable.item(0, 0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("modelSummary", u"Model Version", None));
        ___qtablewidgetitem15 = self.modelProtoTable.item(0, 1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("modelSummary", u"model_version", None));
        ___qtablewidgetitem16 = self.modelProtoTable.item(1, 0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("modelSummary", u"Graph Name", None));
        ___qtablewidgetitem17 = self.modelProtoTable.item(1, 1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("modelSummary", u"graph_name", None));
        ___qtablewidgetitem18 = self.modelProtoTable.item(2, 0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("modelSummary", u"Producer", None));
        ___qtablewidgetitem19 = self.modelProtoTable.item(2, 1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("modelSummary", u"PyTorch 2.1.2", None));
        ___qtablewidgetitem20 = self.modelProtoTable.item(3, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("modelSummary", u"IR Version", None));
        ___qtablewidgetitem21 = self.modelProtoTable.item(3, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("modelSummary", u"ir_version", None));
        self.modelProtoTable.setSortingEnabled(__sortingEnabled)

        self.importsLabel.setText(QCoreApplication.translate("modelSummary", u"<html><head/><body><p><span style=\" font-size:12pt;\">Imports</span></p></body></html>", None))
        ___qtablewidgetitem22 = self.importsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("modelSummary", u"New Column", None));
        ___qtablewidgetitem23 = self.importsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("modelSummary", u"Value", None));
    # retranslateUi

