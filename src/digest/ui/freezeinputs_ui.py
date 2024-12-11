# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'freezeinputs.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFormLayout, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import resource_rc

class Ui_freezeInputs(object):
    def setupUi(self, freezeInputs):
        if not freezeInputs.objectName():
            freezeInputs.setObjectName(u"freezeInputs")
        freezeInputs.resize(902, 692)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(freezeInputs.sizePolicy().hasHeightForWidth())
        freezeInputs.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/assets/images/digest_logo_500.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        freezeInputs.setWindowIcon(icon)
        freezeInputs.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(freezeInputs)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.summaryTopBanner = QWidget(freezeInputs)
        self.summaryTopBanner.setObjectName(u"summaryTopBanner")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.summaryTopBanner.sizePolicy().hasHeightForWidth())
        self.summaryTopBanner.setSizePolicy(sizePolicy1)
        self.summaryTopBannerLayout = QHBoxLayout(self.summaryTopBanner)
        self.summaryTopBannerLayout.setObjectName(u"summaryTopBannerLayout")
        self.summaryTopBannerLayout.setContentsMargins(-1, -1, -1, 0)
        self.titleFrame = QFrame(self.summaryTopBanner)
        self.titleFrame.setObjectName(u"titleFrame")
        self.titleFrame.setAutoFillBackground(False)
        self.titleFrame.setStyleSheet(u"")
        self.titleFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.titleFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.titleFrame)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.titleLabel = QLabel(self.titleFrame)
        self.titleLabel.setObjectName(u"titleLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet(u"")
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setMargin(1)
        self.titleLabel.setIndent(5)
        self.titleLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_17.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignTop)

        self.subtitleLabel = QLabel(self.titleFrame)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.subtitleLabel.setStyleSheet(u"")
        self.subtitleLabel.setMargin(5)

        self.verticalLayout_17.addWidget(self.subtitleLabel)

        self.warningLabel = QLabel(self.titleFrame)
        self.warningLabel.setObjectName(u"warningLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.warningLabel.sizePolicy().hasHeightForWidth())
        self.warningLabel.setSizePolicy(sizePolicy3)
        self.warningLabel.setStyleSheet(u"QLabel {\n"
"    font-size: 10px;\n"
"    background-color: #FFCC00; \n"
"    border: 1px solid #996600; \n"
"    color: #333333;\n"
"    font-weight: bold;\n"
"    border-radius: 0px;\n"
"}")
        self.warningLabel.setMargin(0)

        self.verticalLayout_17.addWidget(self.warningLabel, 0, Qt.AlignmentFlag.AlignTop)


        self.summaryTopBannerLayout.addWidget(self.titleFrame)


        self.verticalLayout.addWidget(self.summaryTopBanner)

        self.frame = QFrame(freezeInputs)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.selectDirBtn = QPushButton(self.frame)
        self.selectDirBtn.setObjectName(u"selectDirBtn")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.selectDirBtn.sizePolicy().hasHeightForWidth())
        self.selectDirBtn.setSizePolicy(sizePolicy4)
        self.selectDirBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.selectDirBtn.setStyleSheet(u"")
        self.selectDirBtn.setAutoExclusive(False)

        self.horizontalLayout.addWidget(self.selectDirBtn, 0, Qt.AlignmentFlag.AlignVCenter)

        self.selectDirLabel = QLabel(self.frame)
        self.selectDirLabel.setObjectName(u"selectDirLabel")
        self.selectDirLabel.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.selectDirLabel, 0, Qt.AlignmentFlag.AlignVCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame)

        self.scrollArea = QScrollArea(freezeInputs)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 882, 526))
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(100)
        sizePolicy6.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy6)
        self.verticalLayout_20 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.dynamicDimsHeader = QLabel(self.scrollAreaWidgetContents)
        self.dynamicDimsHeader.setObjectName(u"dynamicDimsHeader")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.dynamicDimsHeader.sizePolicy().hasHeightForWidth())
        self.dynamicDimsHeader.setSizePolicy(sizePolicy7)
        self.dynamicDimsHeader.setStyleSheet(u"QLabel {\n"
"    font-size: 28px;\n"
"    font-weight: bold;\n"
"	margin-top: 5px;\n"
"	margin-bottom: 5px;\n"
"	color:  #0597F2;\n"
"}")

        self.verticalLayout_20.addWidget(self.dynamicDimsHeader)

        self.dynamicDimsDesc = QLabel(self.scrollAreaWidgetContents)
        self.dynamicDimsDesc.setObjectName(u"dynamicDimsDesc")
        self.dynamicDimsDesc.setStyleSheet(u"")
        self.dynamicDimsDesc.setIndent(10)

        self.verticalLayout_20.addWidget(self.dynamicDimsDesc)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(9, -1, -1, -1)

        self.verticalLayout_20.addLayout(self.formLayout)

        self.applyShapesBtn = QPushButton(self.scrollAreaWidgetContents)
        self.applyShapesBtn.setObjectName(u"applyShapesBtn")
        sizePolicy4.setHeightForWidth(self.applyShapesBtn.sizePolicy().hasHeightForWidth())
        self.applyShapesBtn.setSizePolicy(sizePolicy4)
        self.applyShapesBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.applyShapesBtn.setStyleSheet(u"")
        self.applyShapesBtn.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.applyShapesBtn)

        self.inputsTableHeader = QLabel(self.scrollAreaWidgetContents)
        self.inputsTableHeader.setObjectName(u"inputsTableHeader")
        sizePolicy7.setHeightForWidth(self.inputsTableHeader.sizePolicy().hasHeightForWidth())
        self.inputsTableHeader.setSizePolicy(sizePolicy7)
        self.inputsTableHeader.setStyleSheet(u"QLabel {\n"
"    font-size: 28px;\n"
"    font-weight: bold;\n"
"	margin-top: 5px;\n"
"	margin-bottom: 5px;\n"
"	color:  #0597F2;\n"
"}")

        self.verticalLayout_20.addWidget(self.inputsTableHeader)

        self.inputsTableDesc = QLabel(self.scrollAreaWidgetContents)
        self.inputsTableDesc.setObjectName(u"inputsTableDesc")
        self.inputsTableDesc.setIndent(10)

        self.verticalLayout_20.addWidget(self.inputsTableDesc)

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
        self.inputsTable.setStyleSheet(u"")

        self.verticalLayout_20.addWidget(self.inputsTable)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(freezeInputs)

        QMetaObject.connectSlotsByName(freezeInputs)
    # setupUi

    def retranslateUi(self, freezeInputs):
        freezeInputs.setWindowTitle(QCoreApplication.translate("freezeInputs", u"Form", None))
        self.titleLabel.setText(QCoreApplication.translate("freezeInputs", u"Freeze Input Shapes ", None))
        self.subtitleLabel.setText(QCoreApplication.translate("freezeInputs", u"<html><head/><body><p>Use this utility to set static values for model inputs so shape inference can run</p></body></html>", None))
        self.warningLabel.setText(QCoreApplication.translate("freezeInputs", u"<html><head/><body><p>Warning: Freeze Input Shapes functionality has been disabled because this model did not pass the checker. </p></body></html>", None))
        self.selectDirBtn.setText(QCoreApplication.translate("freezeInputs", u"Select Directory", None))
        self.selectDirLabel.setText(QCoreApplication.translate("freezeInputs", u"Select a directory if you want to save the static graph", None))
        self.dynamicDimsHeader.setText(QCoreApplication.translate("freezeInputs", u"<html><head/><body><p><span style=\" font-size:14pt;\">Dynamic Input Dimensions</span></p></body></html>", None))
        self.dynamicDimsDesc.setText(QCoreApplication.translate("freezeInputs", u"Listed below are the model's dynamic input dimensions. Set each to static value by entering a new value in the text box then click Apply Shapes.", None))
        self.applyShapesBtn.setText(QCoreApplication.translate("freezeInputs", u"Apply Shapes", None))
        self.inputsTableHeader.setText(QCoreApplication.translate("freezeInputs", u"<html><head/><body><p><span style=\" font-size:14pt;\">Input Tensors</span></p></body></html>", None))
        self.inputsTableDesc.setText(QCoreApplication.translate("freezeInputs", u"This table contains all the inputs and dynamic dimensions, use it as a reference for setting the values above.", None))
        ___qtablewidgetitem = self.inputsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("freezeInputs", u"Name", None));
        ___qtablewidgetitem1 = self.inputsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("freezeInputs", u"Shape", None));
        ___qtablewidgetitem2 = self.inputsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("freezeInputs", u"Dtype", None));
        ___qtablewidgetitem3 = self.inputsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("freezeInputs", u"Tensor Size (kB)", None));
    # retranslateUi

