# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'multimodelanalysis.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from histogramchartwidget import HistogramChartWidget

class Ui_multiModelAnalysis(object):
    def setupUi(self, multiModelAnalysis):
        if not multiModelAnalysis.objectName():
            multiModelAnalysis.setObjectName(u"multiModelAnalysis")
        multiModelAnalysis.resize(1085, 866)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(multiModelAnalysis.sizePolicy().hasHeightForWidth())
        multiModelAnalysis.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/assets/images/digest_logo_500.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        multiModelAnalysis.setWindowIcon(icon)
        multiModelAnalysis.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(multiModelAnalysis)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.summaryTopBanner = QWidget(multiModelAnalysis)
        self.summaryTopBanner.setObjectName(u"summaryTopBanner")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.summaryTopBanner.sizePolicy().hasHeightForWidth())
        self.summaryTopBanner.setSizePolicy(sizePolicy1)
        self.summaryTopBannerLayout = QHBoxLayout(self.summaryTopBanner)
        self.summaryTopBannerLayout.setObjectName(u"summaryTopBannerLayout")
        self.modelNameFrame = QFrame(self.summaryTopBanner)
        self.modelNameFrame.setObjectName(u"modelNameFrame")
        self.modelNameFrame.setAutoFillBackground(False)
        self.modelNameFrame.setStyleSheet(u"")
        self.modelNameFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.modelNameFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.modelNameFrame)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.modelName = QLabel(self.modelNameFrame)
        self.modelName.setObjectName(u"modelName")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.modelName.sizePolicy().hasHeightForWidth())
        self.modelName.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setBold(True)
        self.modelName.setFont(font)
        self.modelName.setStyleSheet(u"")
        self.modelName.setWordWrap(True)
        self.modelName.setMargin(1)
        self.modelName.setIndent(5)
        self.modelName.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_17.addWidget(self.modelName)


        self.summaryTopBannerLayout.addWidget(self.modelNameFrame)


        self.verticalLayout.addWidget(self.summaryTopBanner)

        self.frame = QFrame(multiModelAnalysis)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.saveCsvBtn = QPushButton(self.frame)
        self.saveCsvBtn.setObjectName(u"saveCsvBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.saveCsvBtn.sizePolicy().hasHeightForWidth())
        self.saveCsvBtn.setSizePolicy(sizePolicy3)
        self.saveCsvBtn.setMinimumSize(QSize(0, 0))
        self.saveCsvBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveCsvBtn.setStyleSheet(u"")
        self.saveCsvBtn.setAutoExclusive(False)

        self.verticalLayout_2.addWidget(self.saveCsvBtn)

        self.individualCheckBox = QCheckBox(self.frame)
        self.individualCheckBox.setObjectName(u"individualCheckBox")
        self.individualCheckBox.setStyleSheet(u"margin-top: 10px;")
        self.individualCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.individualCheckBox)

        self.multiCheckBox = QCheckBox(self.frame)
        self.multiCheckBox.setObjectName(u"multiCheckBox")
        self.multiCheckBox.setStyleSheet(u"")
        self.multiCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.multiCheckBox)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame)

        self.scrollArea = QScrollArea(multiModelAnalysis)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy4)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1065, 688))
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(100)
        sizePolicy5.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy5)
        self.scrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_20 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.dataTable = QTableWidget(self.scrollAreaWidgetContents)
        self.dataTable.setObjectName(u"dataTable")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(17)
        sizePolicy6.setHeightForWidth(self.dataTable.sizePolicy().hasHeightForWidth())
        self.dataTable.setSizePolicy(sizePolicy6)
        self.dataTable.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.dataTable.setStyleSheet(u"")
        self.dataTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.dataTable.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.dataTable.horizontalHeader().setCascadingSectionResizes(False)
        self.dataTable.horizontalHeader().setProperty(u"showSortIndicator", True)

        self.verticalLayout_20.addWidget(self.dataTable)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy7)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.combinedHistogramFrame = QFrame(self.frame_2)
        self.combinedHistogramFrame.setObjectName(u"combinedHistogramFrame")
        self.combinedHistogramFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.combinedHistogramFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.combinedHistogramFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.opHistogramChart = HistogramChartWidget(self.combinedHistogramFrame)
        self.opHistogramChart.setObjectName(u"opHistogramChart")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.opHistogramChart.sizePolicy().hasHeightForWidth())
        self.opHistogramChart.setSizePolicy(sizePolicy8)
        self.opHistogramChart.setMinimumSize(QSize(500, 300))

        self.verticalLayout_3.addWidget(self.opHistogramChart)


        self.horizontalLayout_2.addWidget(self.combinedHistogramFrame)

        self.stackedHistogramFrame = QFrame(self.frame_2)
        self.stackedHistogramFrame.setObjectName(u"stackedHistogramFrame")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.stackedHistogramFrame.sizePolicy().hasHeightForWidth())
        self.stackedHistogramFrame.setSizePolicy(sizePolicy9)
        self.stackedHistogramFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.stackedHistogramFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.stackedHistogramFrame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.horizontalLayout_2.addWidget(self.stackedHistogramFrame)


        self.verticalLayout_20.addWidget(self.frame_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(multiModelAnalysis)

        QMetaObject.connectSlotsByName(multiModelAnalysis)
    # setupUi

    def retranslateUi(self, multiModelAnalysis):
        multiModelAnalysis.setWindowTitle(QCoreApplication.translate("multiModelAnalysis", u"Form", None))
        self.modelName.setText(QCoreApplication.translate("multiModelAnalysis", u"Multi-Model Analysis", None))
        self.saveCsvBtn.setText(QCoreApplication.translate("multiModelAnalysis", u"Save Reports", None))
        self.individualCheckBox.setText(QCoreApplication.translate("multiModelAnalysis", u"Include Individual Summaries", None))
        self.multiCheckBox.setText(QCoreApplication.translate("multiModelAnalysis", u"Include Multi-Model Summaries", None))
    # retranslateUi

