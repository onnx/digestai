# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pytorchingest.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import resource_rc

class Ui_pytorchIngest(object):
    def setupUi(self, pytorchIngest):
        if not pytorchIngest.objectName():
            pytorchIngest.setObjectName(u"pytorchIngest")
        pytorchIngest.resize(1060, 748)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pytorchIngest.sizePolicy().hasHeightForWidth())
        pytorchIngest.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/assets/images/digest_logo_500.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        pytorchIngest.setWindowIcon(icon)
        pytorchIngest.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(pytorchIngest)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.summaryTopBanner = QWidget(pytorchIngest)
        self.summaryTopBanner.setObjectName(u"summaryTopBanner")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.summaryTopBanner.sizePolicy().hasHeightForWidth())
        self.summaryTopBanner.setSizePolicy(sizePolicy1)
        self.summaryTopBannerLayout = QHBoxLayout(self.summaryTopBanner)
        self.summaryTopBannerLayout.setObjectName(u"summaryTopBannerLayout")
        self.pytorchLogo = QLabel(self.summaryTopBanner)
        self.pytorchLogo.setObjectName(u"pytorchLogo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pytorchLogo.sizePolicy().hasHeightForWidth())
        self.pytorchLogo.setSizePolicy(sizePolicy2)
        self.pytorchLogo.setMaximumSize(QSize(16777215, 16777215))
        self.pytorchLogo.setPixmap(QPixmap(u":/assets/icons/64px-PyTorch_logo_icon.svg.png"))
        self.pytorchLogo.setScaledContents(True)
        self.pytorchLogo.setMargin(5)

        self.summaryTopBannerLayout.addWidget(self.pytorchLogo)

        self.headerFrame = QFrame(self.summaryTopBanner)
        self.headerFrame.setObjectName(u"headerFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.headerFrame.sizePolicy().hasHeightForWidth())
        self.headerFrame.setSizePolicy(sizePolicy3)
        self.headerFrame.setAutoFillBackground(False)
        self.headerFrame.setStyleSheet(u"")
        self.headerFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.headerFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.headerFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.titleLabel = QLabel(self.headerFrame)
        self.titleLabel.setObjectName(u"titleLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy4)
        font = QFont()
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet(u"")
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setMargin(1)
        self.titleLabel.setIndent(5)
        self.titleLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.horizontalLayout.addWidget(self.titleLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.summaryTopBannerLayout.addWidget(self.headerFrame)


        self.verticalLayout.addWidget(self.summaryTopBanner)

        self.scrollArea = QScrollArea(pytorchIngest)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy5)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1040, 616))
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(100)
        sizePolicy6.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy6)
        self.scrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_20 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_20.setSpacing(10)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.modelName = QLabel(self.scrollAreaWidgetContents)
        self.modelName.setObjectName(u"modelName")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.modelName.sizePolicy().hasHeightForWidth())
        self.modelName.setSizePolicy(sizePolicy7)
        self.modelName.setStyleSheet(u"QLabel {\n"
"    font-size: 28px;\n"
"    font-weight: bold;\n"
"	margin-bottom: -5px;\n"
"}")

        self.verticalLayout_20.addWidget(self.modelName)

        self.modelFilename = QLabel(self.scrollAreaWidgetContents)
        self.modelFilename.setObjectName(u"modelFilename")
        self.modelFilename.setMargin(5)

        self.verticalLayout_20.addWidget(self.modelFilename)

        self.selectDirLayout = QHBoxLayout()
        self.selectDirLayout.setSpacing(20)
        self.selectDirLayout.setObjectName(u"selectDirLayout")
        self.selectDirLayout.setContentsMargins(-1, -1, -1, 10)
        self.selectDirBtn = QPushButton(self.scrollAreaWidgetContents)
        self.selectDirBtn.setObjectName(u"selectDirBtn")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.selectDirBtn.sizePolicy().hasHeightForWidth())
        self.selectDirBtn.setSizePolicy(sizePolicy8)
        self.selectDirBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.selectDirBtn.setStyleSheet(u"")
        self.selectDirBtn.setAutoExclusive(False)

        self.selectDirLayout.addWidget(self.selectDirBtn)

        self.selectDirLabel = QLabel(self.scrollAreaWidgetContents)
        self.selectDirLabel.setObjectName(u"selectDirLabel")
        self.selectDirLabel.setStyleSheet(u"")

        self.selectDirLayout.addWidget(self.selectDirLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.selectDirLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_20.addLayout(self.selectDirLayout)

        self.exportOptionsGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.exportOptionsGroupBox.setObjectName(u"exportOptionsGroupBox")
        sizePolicy4.setHeightForWidth(self.exportOptionsGroupBox.sizePolicy().hasHeightForWidth())
        self.exportOptionsGroupBox.setSizePolicy(sizePolicy4)
        font1 = QFont()
        font1.setPointSize(13)
        self.exportOptionsGroupBox.setFont(font1)
        self.exportOptionsGroupBox.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.exportOptionsGroupBox)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 35, -1, 9)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.foldingCheckBox = QCheckBox(self.exportOptionsGroupBox)
        self.foldingCheckBox.setObjectName(u"foldingCheckBox")
        sizePolicy4.setHeightForWidth(self.foldingCheckBox.sizePolicy().hasHeightForWidth())
        self.foldingCheckBox.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setPointSize(10)
        self.foldingCheckBox.setFont(font2)
        self.foldingCheckBox.setChecked(True)

        self.horizontalLayout_3.addWidget(self.foldingCheckBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.exportParamsCheckBox = QCheckBox(self.exportOptionsGroupBox)
        self.exportParamsCheckBox.setObjectName(u"exportParamsCheckBox")
        sizePolicy4.setHeightForWidth(self.exportParamsCheckBox.sizePolicy().hasHeightForWidth())
        self.exportParamsCheckBox.setSizePolicy(sizePolicy4)
        self.exportParamsCheckBox.setFont(font2)
        self.exportParamsCheckBox.setChecked(True)

        self.horizontalLayout_4.addWidget(self.exportParamsCheckBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.opsetLayout = QHBoxLayout()
        self.opsetLayout.setObjectName(u"opsetLayout")
        self.opsetLabel = QLabel(self.exportOptionsGroupBox)
        self.opsetLabel.setObjectName(u"opsetLabel")
        sizePolicy2.setHeightForWidth(self.opsetLabel.sizePolicy().hasHeightForWidth())
        self.opsetLabel.setSizePolicy(sizePolicy2)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(False)
        self.opsetLabel.setFont(font3)

        self.opsetLayout.addWidget(self.opsetLabel)

        self.opsetInfoLabel = QLabel(self.exportOptionsGroupBox)
        self.opsetInfoLabel.setObjectName(u"opsetInfoLabel")
        sizePolicy2.setHeightForWidth(self.opsetInfoLabel.sizePolicy().hasHeightForWidth())
        self.opsetInfoLabel.setSizePolicy(sizePolicy2)
        font4 = QFont()
        font4.setPointSize(10)
        font4.setItalic(False)
        self.opsetInfoLabel.setFont(font4)
        self.opsetInfoLabel.setMargin(0)

        self.opsetLayout.addWidget(self.opsetInfoLabel)

        self.opsetLineEdit = QLineEdit(self.exportOptionsGroupBox)
        self.opsetLineEdit.setObjectName(u"opsetLineEdit")
        sizePolicy2.setHeightForWidth(self.opsetLineEdit.sizePolicy().hasHeightForWidth())
        self.opsetLineEdit.setSizePolicy(sizePolicy2)
        self.opsetLineEdit.setMaximumSize(QSize(35, 16777215))
        self.opsetLineEdit.setFont(font2)

        self.opsetLayout.addWidget(self.opsetLineEdit)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.opsetLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.opsetLayout)


        self.verticalLayout_20.addWidget(self.exportOptionsGroupBox)

        self.inputsGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.inputsGroupBox.setObjectName(u"inputsGroupBox")
        font5 = QFont()
        font5.setPointSize(14)
        self.inputsGroupBox.setFont(font5)
        self.verticalLayout_3 = QVBoxLayout(self.inputsGroupBox)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 25, -1, -1)
        self.label = QLabel(self.inputsGroupBox)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setPointSize(12)
        self.label.setFont(font6)
        self.label.setStyleSheet(u"color: lightgrey;")
        self.label.setWordWrap(True)
        self.label.setMargin(5)

        self.verticalLayout_3.addWidget(self.label)

        self.inputsFormLayout = QFormLayout()
        self.inputsFormLayout.setObjectName(u"inputsFormLayout")
        self.inputsFormLayout.setContentsMargins(20, -1, -1, -1)

        self.verticalLayout_3.addLayout(self.inputsFormLayout)


        self.verticalLayout_20.addWidget(self.inputsGroupBox)

        self.exportWarningLabel = QLabel(self.scrollAreaWidgetContents)
        self.exportWarningLabel.setObjectName(u"exportWarningLabel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.exportWarningLabel.sizePolicy().hasHeightForWidth())
        self.exportWarningLabel.setSizePolicy(sizePolicy9)
        self.exportWarningLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 10px;\n"
"    background-color: #FFCC00; \n"
"    border: 1px solid #996600; \n"
"    color: #333333;\n"
"    font-weight: bold;\n"
"    border-radius: 0px;\n"
"}")
        self.exportWarningLabel.setMargin(5)

        self.verticalLayout_20.addWidget(self.exportWarningLabel)

        self.exportOnnxBtn = QPushButton(self.scrollAreaWidgetContents)
        self.exportOnnxBtn.setObjectName(u"exportOnnxBtn")
        sizePolicy8.setHeightForWidth(self.exportOnnxBtn.sizePolicy().hasHeightForWidth())
        self.exportOnnxBtn.setSizePolicy(sizePolicy8)
        self.exportOnnxBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.exportOnnxBtn.setStyleSheet(u"")
        self.exportOnnxBtn.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.exportOnnxBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_20.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(pytorchIngest)

        QMetaObject.connectSlotsByName(pytorchIngest)
    # setupUi

    def retranslateUi(self, pytorchIngest):
        pytorchIngest.setWindowTitle(QCoreApplication.translate("pytorchIngest", u"Form", None))
        self.pytorchLogo.setText("")
        self.titleLabel.setText(QCoreApplication.translate("pytorchIngest", u"PyTorch Ingest", None))
        self.modelName.setText(QCoreApplication.translate("pytorchIngest", u"model name", None))
        self.modelFilename.setText(QCoreApplication.translate("pytorchIngest", u"path to the model file", None))
        self.selectDirBtn.setText(QCoreApplication.translate("pytorchIngest", u"Select Directory", None))
        self.selectDirLabel.setText(QCoreApplication.translate("pytorchIngest", u"Select a directory if you would like to save the ONNX model file", None))
        self.exportOptionsGroupBox.setTitle(QCoreApplication.translate("pytorchIngest", u"Export Options", None))
        self.foldingCheckBox.setText(QCoreApplication.translate("pytorchIngest", u"Do constant folding", None))
        self.exportParamsCheckBox.setText(QCoreApplication.translate("pytorchIngest", u"Export params", None))
        self.opsetLabel.setText(QCoreApplication.translate("pytorchIngest", u"Opset", None))
        self.opsetInfoLabel.setText(QCoreApplication.translate("pytorchIngest", u"(accepted range is 7 - 21):", None))
        self.opsetLineEdit.setText(QCoreApplication.translate("pytorchIngest", u"17", None))
        self.inputsGroupBox.setTitle(QCoreApplication.translate("pytorchIngest", u"Inputs", None))
        self.label.setText(QCoreApplication.translate("pytorchIngest", u"The following inputs were taken from the PyTorch model's forward function. Please set the dimensions for each input needed. Dimensions can be set by specifying a combination of symbolic and integer values separated by a comma, for example: batch_size, 3, 224, 244.", None))
        self.exportWarningLabel.setText(QCoreApplication.translate("pytorchIngest", u"<html><head/><body><p>This is a warning message that we can use for now to prompt the user.</p></body></html>", None))
        self.exportOnnxBtn.setText(QCoreApplication.translate("pytorchIngest", u"Export ONNX", None))
    # retranslateUi

