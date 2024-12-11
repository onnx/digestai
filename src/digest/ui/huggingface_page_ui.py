# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'huggingface_page.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTreeView,
    QVBoxLayout, QWidget)

from plaintexteditentersignal import PlainTextEditEnterSignal
import resource_rc

class Ui_huggingfacePage(object):
    def setupUi(self, huggingfacePage):
        if not huggingfacePage.objectName():
            huggingfacePage.setObjectName(u"huggingfacePage")
        huggingfacePage.resize(845, 600)
        huggingfacePage.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(huggingfacePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(huggingfacePage)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.hfLogo = QLabel(self.frame)
        self.hfLogo.setObjectName(u"hfLogo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.hfLogo.sizePolicy().hasHeightForWidth())
        self.hfLogo.setSizePolicy(sizePolicy1)
        self.hfLogo.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setPointSize(8)
        self.hfLogo.setFont(font)
        self.hfLogo.setStyleSheet(u"")
        self.hfLogo.setPixmap(QPixmap(u":/assets/icons/huggingface_64px.png"))
        self.hfLogo.setMargin(5)

        self.horizontalLayout_2.addWidget(self.hfLogo, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.hf_search_text = PlainTextEditEnterSignal(self.frame)
        self.hf_search_text.setObjectName(u"hf_search_text")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.hf_search_text.sizePolicy().hasHeightForWidth())
        self.hf_search_text.setSizePolicy(sizePolicy2)
        self.hf_search_text.setMinimumSize(QSize(500, 0))
        self.hf_search_text.setMaximumSize(QSize(16777215, 40))
        self.hf_search_text.setStyleSheet(u"QPlainTextEdit {\n"
"    background-color: #282828; \n"
"    color: #F8F8F2;\n"
"    border: 1px solid #444444;\n"
"    padding: 8px;\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPlainTextEdit:focus {\n"
"    border: 1px solid #6272A4;\n"
"}\n"
"\n"
"QPlainTextEdit::handle:vertical:hover {\n"
"    background-color: #686868;\n"
"}\n"
"\n"
"QPlainTextEdit:placeholderText {\n"
"    color: #6272A4; \n"
"}\n"
"\n"
"QTextEdit:placeholderText {\n"
"    color: #6272A4; \n"
"	font: italic 9pt;\n"
"}")
        self.hf_search_text.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.hf_search_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.hf_search_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.hf_search_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.hf_search_text.setMaximumBlockCount(1)

        self.horizontalLayout_2.addWidget(self.hf_search_text, 0, Qt.AlignmentFlag.AlignVCenter)

        self.hf_search_btn = QPushButton(self.frame)
        self.hf_search_btn.setObjectName(u"hf_search_btn")
        sizePolicy2.setHeightForWidth(self.hf_search_btn.sizePolicy().hasHeightForWidth())
        self.hf_search_btn.setSizePolicy(sizePolicy2)
        self.hf_search_btn.setMinimumSize(QSize(0, 40))
        self.hf_search_btn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	border: 1px solid rgb(60, 60, 60); \n"
"	padding: 5px 5px;\n"
"	border-radius: 5px;\n"
"	background-color: rgb(80, 80, 80); \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(255, 210, 30); \n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(255, 225, 30)\n"
"}   ")
        icon = QIcon()
        icon.addFile(u":/assets/icons/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.hf_search_btn.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.hf_search_btn, 0, Qt.AlignmentFlag.AlignVCenter)

        self.hf_info_label_2 = QLabel(self.frame)
        self.hf_info_label_2.setObjectName(u"hf_info_label_2")
        self.hf_info_label_2.setStyleSheet(u"")
        self.hf_info_label_2.setMargin(10)

        self.horizontalLayout_2.addWidget(self.hf_info_label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.open_onnx_btn = QPushButton(huggingfacePage)
        self.open_onnx_btn.setObjectName(u"open_onnx_btn")
        self.open_onnx_btn.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.open_onnx_btn.sizePolicy().hasHeightForWidth())
        self.open_onnx_btn.setSizePolicy(sizePolicy1)
        self.open_onnx_btn.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.open_onnx_btn, 0, Qt.AlignmentFlag.AlignVCenter)

        self.hf_info_label = QLabel(huggingfacePage)
        self.hf_info_label.setObjectName(u"hf_info_label")
        self.hf_info_label.setMargin(10)

        self.horizontalLayout_3.addWidget(self.hf_info_label)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.hf_column_view = QTreeView(huggingfacePage)
        self.hf_column_view.setObjectName(u"hf_column_view")
        self.hf_column_view.setStyleSheet(u"")
        self.hf_column_view.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.hf_column_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.hf_column_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.hf_column_view.setRootIsDecorated(True)
        self.hf_column_view.setAnimated(False)
        self.hf_column_view.setAllColumnsShowFocus(True)
        self.hf_column_view.setHeaderHidden(True)
        self.hf_column_view.header().setVisible(False)

        self.verticalLayout.addWidget(self.hf_column_view)


        self.retranslateUi(huggingfacePage)

        QMetaObject.connectSlotsByName(huggingfacePage)
    # setupUi

    def retranslateUi(self, huggingfacePage):
        huggingfacePage.setWindowTitle(QCoreApplication.translate("huggingfacePage", u"Form", None))
        self.hfLogo.setText("")
        self.hf_search_text.setPlainText("")
        self.hf_search_text.setPlaceholderText(QCoreApplication.translate("huggingfacePage", u"Huggingface checkpoint or url...", None))
#if QT_CONFIG(tooltip)
        self.hf_search_btn.setToolTip(QCoreApplication.translate("huggingfacePage", u"Search (Enter)", None))
#endif // QT_CONFIG(tooltip)
        self.hf_search_btn.setText("")
#if QT_CONFIG(shortcut)
        self.hf_search_btn.setShortcut(QCoreApplication.translate("huggingfacePage", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.hf_info_label_2.setText(QCoreApplication.translate("huggingfacePage", u"\u26a0\ufe0f This feature is still in beta. ", None))
        self.open_onnx_btn.setText(QCoreApplication.translate("huggingfacePage", u"Open ONNX", None))
        self.hf_info_label.setText(QCoreApplication.translate("huggingfacePage", u"\u2139\ufe0f TextLabel", None))
    # retranslateUi

