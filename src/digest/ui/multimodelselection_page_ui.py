# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'multimodelselection_page.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MultiModelSelection(object):
    def setupUi(self, MultiModelSelection):
        if not MultiModelSelection.objectName():
            MultiModelSelection.setObjectName(u"MultiModelSelection")
        MultiModelSelection.resize(1062, 816)
        MultiModelSelection.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(MultiModelSelection)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLayout = QVBoxLayout()
        self.titleLayout.setSpacing(0)
        self.titleLayout.setObjectName(u"titleLayout")
        self.titleLabel = QLabel(MultiModelSelection)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setStyleSheet(u"")
        self.titleLabel.setMargin(10)

        self.titleLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(MultiModelSelection)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.subtitleLabel.setStyleSheet(u"")
        self.subtitleLabel.setMargin(5)

        self.titleLayout.addWidget(self.subtitleLabel)


        self.verticalLayout.addLayout(self.titleLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.selectFolderBtn = QPushButton(MultiModelSelection)
        self.selectFolderBtn.setObjectName(u"selectFolderBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectFolderBtn.sizePolicy().hasHeightForWidth())
        self.selectFolderBtn.setSizePolicy(sizePolicy)
        self.selectFolderBtn.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.selectFolderBtn)

        self.openAnalysisBtn = QPushButton(MultiModelSelection)
        self.openAnalysisBtn.setObjectName(u"openAnalysisBtn")
        self.openAnalysisBtn.setEnabled(False)
        sizePolicy.setHeightForWidth(self.openAnalysisBtn.sizePolicy().hasHeightForWidth())
        self.openAnalysisBtn.setSizePolicy(sizePolicy)
        self.openAnalysisBtn.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.openAnalysisBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.infoLabel = QLabel(MultiModelSelection)
        self.infoLabel.setObjectName(u"infoLabel")
        self.infoLabel.setStyleSheet(u"background: transparent;\n"
"")
        self.infoLabel.setMargin(6)

        self.verticalLayout.addWidget(self.infoLabel)

        self.warningLabel = QLabel(MultiModelSelection)
        self.warningLabel.setObjectName(u"warningLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.warningLabel.sizePolicy().hasHeightForWidth())
        self.warningLabel.setSizePolicy(sizePolicy1)
        self.warningLabel.setStyleSheet(u"")
        self.warningLabel.setMargin(2)

        self.verticalLayout.addWidget(self.warningLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioAll = QRadioButton(MultiModelSelection)
        self.radioAll.setObjectName(u"radioAll")
        sizePolicy.setHeightForWidth(self.radioAll.sizePolicy().hasHeightForWidth())
        self.radioAll.setSizePolicy(sizePolicy)
        self.radioAll.setMinimumSize(QSize(0, 33))
        self.radioAll.setAutoFillBackground(False)
        self.radioAll.setStyleSheet(u"")
        self.radioAll.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radioAll)

        self.radioONNX = QRadioButton(MultiModelSelection)
        self.radioONNX.setObjectName(u"radioONNX")
        sizePolicy.setHeightForWidth(self.radioONNX.sizePolicy().hasHeightForWidth())
        self.radioONNX.setSizePolicy(sizePolicy)
        self.radioONNX.setMinimumSize(QSize(0, 33))
        self.radioONNX.setAutoFillBackground(False)
        self.radioONNX.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.radioONNX)

        self.radioReports = QRadioButton(MultiModelSelection)
        self.radioReports.setObjectName(u"radioReports")
        sizePolicy.setHeightForWidth(self.radioReports.sizePolicy().hasHeightForWidth())
        self.radioReports.setSizePolicy(sizePolicy)
        self.radioReports.setMinimumSize(QSize(0, 33))
        self.radioReports.setAutoFillBackground(False)
        self.radioReports.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.radioReports)

        self.duplicateLabel = QLabel(MultiModelSelection)
        self.duplicateLabel.setObjectName(u"duplicateLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.duplicateLabel.sizePolicy().hasHeightForWidth())
        self.duplicateLabel.setSizePolicy(sizePolicy2)
        self.duplicateLabel.setMinimumSize(QSize(550, 0))
        self.duplicateLabel.setStyleSheet(u"")
        self.duplicateLabel.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.duplicateLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.numSelectedLabel = QLabel(MultiModelSelection)
        self.numSelectedLabel.setObjectName(u"numSelectedLabel")
        self.numSelectedLabel.setStyleSheet(u"")
        self.numSelectedLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.numSelectedLabel)

        self.columnsLayout = QHBoxLayout()
        self.columnsLayout.setObjectName(u"columnsLayout")
        self.leftColumnLayout = QVBoxLayout()
        self.leftColumnLayout.setObjectName(u"leftColumnLayout")
        self.modelListView = QListView(MultiModelSelection)
        self.modelListView.setObjectName(u"modelListView")
        self.modelListView.setStyleSheet(u"")
        self.modelListView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.modelListView.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.modelListView.setSpacing(2)

        self.leftColumnLayout.addWidget(self.modelListView)


        self.columnsLayout.addLayout(self.leftColumnLayout)

        self.rightColumnLayout = QVBoxLayout()
        self.rightColumnLayout.setObjectName(u"rightColumnLayout")
        self.duplicateListWidget = QListWidget(MultiModelSelection)
        self.duplicateListWidget.setObjectName(u"duplicateListWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.duplicateListWidget.sizePolicy().hasHeightForWidth())
        self.duplicateListWidget.setSizePolicy(sizePolicy3)
        self.duplicateListWidget.setStyleSheet(u"")
        self.duplicateListWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.duplicateListWidget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.duplicateListWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerItem)
        self.duplicateListWidget.setMovement(QListView.Movement.Static)
        self.duplicateListWidget.setSpacing(2)

        self.rightColumnLayout.addWidget(self.duplicateListWidget)


        self.columnsLayout.addLayout(self.rightColumnLayout)


        self.verticalLayout.addLayout(self.columnsLayout)


        self.retranslateUi(MultiModelSelection)

        QMetaObject.connectSlotsByName(MultiModelSelection)
    # setupUi

    def retranslateUi(self, MultiModelSelection):
        MultiModelSelection.setWindowTitle(QCoreApplication.translate("MultiModelSelection", u"Form", None))
        self.titleLabel.setText(QCoreApplication.translate("MultiModelSelection", u"Multi-Model Selection", None))
        self.subtitleLabel.setText(QCoreApplication.translate("MultiModelSelection", u"<html><head/><body><p><span style=\" font-size:12pt;\">Select a folder to open multiple models for analysis</span></p></body></html>", None))
        self.selectFolderBtn.setText(QCoreApplication.translate("MultiModelSelection", u"Select Folder", None))
        self.openAnalysisBtn.setText(QCoreApplication.translate("MultiModelSelection", u"Open Analysis", None))
        self.infoLabel.setText("")
        self.warningLabel.setText(QCoreApplication.translate("MultiModelSelection", u"Warning", None))
        self.radioAll.setText(QCoreApplication.translate("MultiModelSelection", u"All", None))
        self.radioONNX.setText(QCoreApplication.translate("MultiModelSelection", u"ONNX", None))
        self.radioReports.setText(QCoreApplication.translate("MultiModelSelection", u"Reports", None))
        self.duplicateLabel.setText(QCoreApplication.translate("MultiModelSelection", u"The following models were found to be duplicates and have been deselected from the list on the left.", None))
        self.numSelectedLabel.setText(QCoreApplication.translate("MultiModelSelection", u"0 selected models", None))
    # retranslateUi

