# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nodessummary.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_nodesSummary(object):
    def setupUi(self, nodesSummary):
        if not nodesSummary.objectName():
            nodesSummary.setObjectName(u"nodesSummary")
        nodesSummary.resize(908, 647)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(nodesSummary.sizePolicy().hasHeightForWidth())
        nodesSummary.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/assets/images/digest_logo_500.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        nodesSummary.setWindowIcon(icon)
        nodesSummary.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(nodesSummary)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.summaryTopBanner = QWidget(nodesSummary)
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

        self.verticalLayout_17.addWidget(self.modelName, 0, Qt.AlignmentFlag.AlignTop)


        self.summaryTopBannerLayout.addWidget(self.modelNameFrame)


        self.verticalLayout.addWidget(self.summaryTopBanner)

        self.frame = QFrame(nodesSummary)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveCsvBtn = QPushButton(self.frame)
        self.saveCsvBtn.setObjectName(u"saveCsvBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.saveCsvBtn.sizePolicy().hasHeightForWidth())
        self.saveCsvBtn.setSizePolicy(sizePolicy3)
        self.saveCsvBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveCsvBtn.setStyleSheet(u"")
        self.saveCsvBtn.setAutoExclusive(False)

        self.horizontalLayout.addWidget(self.saveCsvBtn)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.allNodesBtn = QPushButton(self.frame)
        self.allNodesBtn.setObjectName(u"allNodesBtn")
        sizePolicy3.setHeightForWidth(self.allNodesBtn.sizePolicy().hasHeightForWidth())
        self.allNodesBtn.setSizePolicy(sizePolicy3)
        self.allNodesBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.allNodesBtn.setStyleSheet(u"")
        self.allNodesBtn.setCheckable(True)
        self.allNodesBtn.setChecked(True)
        self.allNodesBtn.setAutoExclusive(True)

        self.horizontalLayout.addWidget(self.allNodesBtn)

        self.shapeCountsBtn = QPushButton(self.frame)
        self.shapeCountsBtn.setObjectName(u"shapeCountsBtn")
        sizePolicy3.setHeightForWidth(self.shapeCountsBtn.sizePolicy().hasHeightForWidth())
        self.shapeCountsBtn.setSizePolicy(sizePolicy3)
        self.shapeCountsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.shapeCountsBtn.setStyleSheet(u"")
        self.shapeCountsBtn.setCheckable(True)
        self.shapeCountsBtn.setAutoExclusive(True)

        self.horizontalLayout.addWidget(self.shapeCountsBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame)

        self.scrollArea = QScrollArea(nodesSummary)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 888, 512))
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(100)
        sizePolicy5.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy5)
        self.verticalLayout_20 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.dataTable = QTableWidget(self.scrollAreaWidgetContents)
        self.dataTable.setObjectName(u"dataTable")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(17)
        sizePolicy6.setHeightForWidth(self.dataTable.sizePolicy().hasHeightForWidth())
        self.dataTable.setSizePolicy(sizePolicy6)
        self.dataTable.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.dataTable.setStyleSheet(u"")
        self.dataTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.dataTable.horizontalHeader().setCascadingSectionResizes(False)
        self.dataTable.horizontalHeader().setProperty(u"showSortIndicator", True)

        self.verticalLayout_20.addWidget(self.dataTable)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(nodesSummary)

        QMetaObject.connectSlotsByName(nodesSummary)
    # setupUi

    def retranslateUi(self, nodesSummary):
        nodesSummary.setWindowTitle(QCoreApplication.translate("nodesSummary", u"Form", None))
        self.modelName.setText(QCoreApplication.translate("nodesSummary", u"modelName", None))
        self.saveCsvBtn.setText(QCoreApplication.translate("nodesSummary", u"Save Table (csv)", None))
        self.allNodesBtn.setText(QCoreApplication.translate("nodesSummary", u"All Nodes", None))
        self.shapeCountsBtn.setText(QCoreApplication.translate("nodesSummary", u"Shape Counts", None))
    # retranslateUi

