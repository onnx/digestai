# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(864, 783)
        icon = QIcon()
        icon.addFile(u":/assets/images/digest_logo_500.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.horizontalLayout_5 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.leftPanelWidget = QWidget(self.centralwidget)
        self.leftPanelWidget.setObjectName(u"leftPanelWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftPanelWidget.sizePolicy().hasHeightForWidth())
        self.leftPanelWidget.setSizePolicy(sizePolicy)
        self.leftPanelWidget.setMinimumSize(QSize(85, 0))
        self.leftPanelWidget.setMaximumSize(QSize(16777215, 16777215))
        self.leftPanelWidget.setStyleSheet(u"")
        self.verticalLayout_7 = QVBoxLayout(self.leftPanelWidget)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.iconGroup = QWidget(self.leftPanelWidget)
        self.iconGroup.setObjectName(u"iconGroup")
        sizePolicy.setHeightForWidth(self.iconGroup.sizePolicy().hasHeightForWidth())
        self.iconGroup.setSizePolicy(sizePolicy)
        self.iconGroup.setMinimumSize(QSize(0, 0))
        self.verticalLayout_8 = QVBoxLayout(self.iconGroup)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(5, -1, 5, -1)
        self.logoBtn = QPushButton(self.iconGroup)
        self.logoBtn.setObjectName(u"logoBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logoBtn.sizePolicy().hasHeightForWidth())
        self.logoBtn.setSizePolicy(sizePolicy1)
        self.logoBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.logoBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"    border: 0px;\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/assets/images/remove_background_500_zoom.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logoBtn.setIcon(icon1)
        self.logoBtn.setIconSize(QSize(44, 44))
        self.logoBtn.setCheckable(False)
        self.logoBtn.setAutoExclusive(True)

        self.verticalLayout_8.addWidget(self.logoBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.ingestLine_2 = QFrame(self.iconGroup)
        self.ingestLine_2.setObjectName(u"ingestLine_2")
        sizePolicy1.setHeightForWidth(self.ingestLine_2.sizePolicy().hasHeightForWidth())
        self.ingestLine_2.setSizePolicy(sizePolicy1)
        self.ingestLine_2.setMinimumSize(QSize(50, 0))
        self.ingestLine_2.setStyleSheet(u"color: rgb(100,100,100)")
        self.ingestLine_2.setFrameShadow(QFrame.Shadow.Plain)
        self.ingestLine_2.setLineWidth(2)
        self.ingestLine_2.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_8.addWidget(self.ingestLine_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.ingestWidget = QWidget(self.iconGroup)
        self.ingestWidget.setObjectName(u"ingestWidget")
        sizePolicy.setHeightForWidth(self.ingestWidget.sizePolicy().hasHeightForWidth())
        self.ingestWidget.setSizePolicy(sizePolicy)
        self.ingestLayout = QVBoxLayout(self.ingestWidget)
        self.ingestLayout.setSpacing(15)
        self.ingestLayout.setObjectName(u"ingestLayout")
        self.ingestLayout.setContentsMargins(-1, 10, -1, -1)
        self.openFileBtn = QPushButton(self.ingestWidget)
        self.openFileBtn.setObjectName(u"openFileBtn")
        sizePolicy1.setHeightForWidth(self.openFileBtn.sizePolicy().hasHeightForWidth())
        self.openFileBtn.setSizePolicy(sizePolicy1)
        self.openFileBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.openFileBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.openFileBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"    border: 0px;\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/assets/icons/file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.openFileBtn.setIcon(icon2)
        self.openFileBtn.setIconSize(QSize(34, 34))
        self.openFileBtn.setCheckable(False)
        self.openFileBtn.setAutoExclusive(False)

        self.ingestLayout.addWidget(self.openFileBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.openFolderBtn = QPushButton(self.ingestWidget)
        self.openFolderBtn.setObjectName(u"openFolderBtn")
        sizePolicy1.setHeightForWidth(self.openFolderBtn.sizePolicy().hasHeightForWidth())
        self.openFolderBtn.setSizePolicy(sizePolicy1)
        self.openFolderBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.openFolderBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.openFolderBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"    border: 0px;\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/assets/icons/models.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.openFolderBtn.setIcon(icon3)
        self.openFolderBtn.setIconSize(QSize(34, 34))
        self.openFolderBtn.setCheckable(True)
        self.openFolderBtn.setAutoExclusive(False)

        self.ingestLayout.addWidget(self.openFolderBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.huggingfaceBtn = QPushButton(self.ingestWidget)
        self.huggingfaceBtn.setObjectName(u"huggingfaceBtn")
        sizePolicy1.setHeightForWidth(self.huggingfaceBtn.sizePolicy().hasHeightForWidth())
        self.huggingfaceBtn.setSizePolicy(sizePolicy1)
        self.huggingfaceBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.huggingfaceBtn.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.huggingfaceBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"    border: 0px;\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/assets/icons/huggingface.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.huggingfaceBtn.setIcon(icon4)
        self.huggingfaceBtn.setIconSize(QSize(36, 36))
        self.huggingfaceBtn.setCheckable(True)
        self.huggingfaceBtn.setAutoExclusive(False)

        self.ingestLayout.addWidget(self.huggingfaceBtn, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_8.addWidget(self.ingestWidget, 0, Qt.AlignmentFlag.AlignHCenter)

        self.singleModelWidget = QWidget(self.iconGroup)
        self.singleModelWidget.setObjectName(u"singleModelWidget")
        self.singleModelToolsLayout = QVBoxLayout(self.singleModelWidget)
        self.singleModelToolsLayout.setObjectName(u"singleModelToolsLayout")
        self.ingestLine = QFrame(self.singleModelWidget)
        self.ingestLine.setObjectName(u"ingestLine")
        sizePolicy1.setHeightForWidth(self.ingestLine.sizePolicy().hasHeightForWidth())
        self.ingestLine.setSizePolicy(sizePolicy1)
        self.ingestLine.setMinimumSize(QSize(50, 0))
        self.ingestLine.setStyleSheet(u"color: rgb(100,100,100)")
        self.ingestLine.setFrameShadow(QFrame.Shadow.Plain)
        self.ingestLine.setLineWidth(2)
        self.ingestLine.setFrameShape(QFrame.Shape.HLine)

        self.singleModelToolsLayout.addWidget(self.ingestLine, 0, Qt.AlignmentFlag.AlignHCenter)

        self.summaryBtn = QPushButton(self.singleModelWidget)
        self.summaryBtn.setObjectName(u"summaryBtn")
        sizePolicy1.setHeightForWidth(self.summaryBtn.sizePolicy().hasHeightForWidth())
        self.summaryBtn.setSizePolicy(sizePolicy1)
        self.summaryBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.summaryBtn.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.summaryBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	border: 1px solid rgba(60, 60, 60, 0.8);\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon5 = QIcon()
        icon5.addFile(u":/assets/icons/summary.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.summaryBtn.setIcon(icon5)
        self.summaryBtn.setIconSize(QSize(32, 32))
        self.summaryBtn.setCheckable(True)
        self.summaryBtn.setAutoExclusive(False)

        self.singleModelToolsLayout.addWidget(self.summaryBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.saveBtn = QPushButton(self.singleModelWidget)
        self.saveBtn.setObjectName(u"saveBtn")
        sizePolicy1.setHeightForWidth(self.saveBtn.sizePolicy().hasHeightForWidth())
        self.saveBtn.setSizePolicy(sizePolicy1)
        self.saveBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.saveBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	border: 1px solid rgba(60, 60, 60, 0.8);\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon6 = QIcon()
        icon6.addFile(u":/assets/icons/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.saveBtn.setIcon(icon6)
        self.saveBtn.setIconSize(QSize(32, 32))
        self.saveBtn.setCheckable(False)
        self.saveBtn.setAutoExclusive(False)

        self.singleModelToolsLayout.addWidget(self.saveBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.nodesListBtn = QPushButton(self.singleModelWidget)
        self.nodesListBtn.setObjectName(u"nodesListBtn")
        sizePolicy1.setHeightForWidth(self.nodesListBtn.sizePolicy().hasHeightForWidth())
        self.nodesListBtn.setSizePolicy(sizePolicy1)
        self.nodesListBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.nodesListBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.nodesListBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	border: 1px solid rgba(60, 60, 60, 0.8);\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon7 = QIcon()
        icon7.addFile(u":/assets/icons/node_list.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nodesListBtn.setIcon(icon7)
        self.nodesListBtn.setIconSize(QSize(32, 32))
        self.nodesListBtn.setCheckable(False)
        self.nodesListBtn.setAutoExclusive(False)

        self.singleModelToolsLayout.addWidget(self.nodesListBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.subgraphBtn = QPushButton(self.singleModelWidget)
        self.subgraphBtn.setObjectName(u"subgraphBtn")
        sizePolicy1.setHeightForWidth(self.subgraphBtn.sizePolicy().hasHeightForWidth())
        self.subgraphBtn.setSizePolicy(sizePolicy1)
        self.subgraphBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.subgraphBtn.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.subgraphBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	border: 1px solid rgba(60, 60, 60, 0.8);\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon8 = QIcon()
        icon8.addFile(u":/assets/icons/subgraph.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.subgraphBtn.setIcon(icon8)
        self.subgraphBtn.setIconSize(QSize(28, 28))
        self.subgraphBtn.setCheckable(True)
        self.subgraphBtn.setAutoExclusive(False)

        self.singleModelToolsLayout.addWidget(self.subgraphBtn, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_8.addWidget(self.singleModelWidget)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)


        self.verticalLayout_7.addWidget(self.iconGroup)

        self.iconSpacer = QSpacerItem(10, 375, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.iconSpacer)

        self.bottomFrame = QFrame(self.leftPanelWidget)
        self.bottomFrame.setObjectName(u"bottomFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.bottomFrame.sizePolicy().hasHeightForWidth())
        self.bottomFrame.setSizePolicy(sizePolicy2)
        self.bottomFrame.setAutoFillBackground(False)
        self.bottomFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.bottomFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.bottomFrame)
        self.verticalLayout_6.setSpacing(20)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(8, -1, -1, -1)
        self.infoBtn = QPushButton(self.bottomFrame)
        self.infoBtn.setObjectName(u"infoBtn")
        sizePolicy1.setHeightForWidth(self.infoBtn.sizePolicy().hasHeightForWidth())
        self.infoBtn.setSizePolicy(sizePolicy1)
        self.infoBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.infoBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.infoBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"    border: 0px;\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon9 = QIcon()
        icon9.addFile(u":/assets/icons/info.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.infoBtn.setIcon(icon9)
        self.infoBtn.setIconSize(QSize(24, 24))
        self.infoBtn.setCheckable(False)
        self.infoBtn.setAutoExclusive(True)

        self.verticalLayout_6.addWidget(self.infoBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.exitBtn = QPushButton(self.bottomFrame)
        self.exitBtn.setObjectName(u"exitBtn")
        sizePolicy1.setHeightForWidth(self.exitBtn.sizePolicy().hasHeightForWidth())
        self.exitBtn.setSizePolicy(sizePolicy1)
        self.exitBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.exitBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.exitBtn.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"    border: 0px;\n"
"	padding: 8px 8px;\n"
"	border-radius: 5px;\n"
"	margin-top: 5px;\n"
"}\n"
"")
        icon10 = QIcon()
        icon10.addFile(u":/assets/icons/close-window-64.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitBtn.setIcon(icon10)
        self.exitBtn.setIconSize(QSize(24, 24))

        self.verticalLayout_6.addWidget(self.exitBtn, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_7.addWidget(self.bottomFrame, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_5.addWidget(self.leftPanelWidget)

        self.appContentArea = QWidget(self.centralwidget)
        self.appContentArea.setObjectName(u"appContentArea")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.appContentArea.sizePolicy().hasHeightForWidth())
        self.appContentArea.setSizePolicy(sizePolicy3)
        self.appContentArea.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.appContentArea)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(5, 0, 0, 0)
        self.appHeaderWidget = QWidget(self.appContentArea)
        self.appHeaderWidget.setObjectName(u"appHeaderWidget")
        self.appHeaderWidget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.appHeaderWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout_13.addWidget(self.appHeaderWidget)

        self.stackedWidget = QStackedWidget(self.appContentArea)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setAcceptDrops(True)
        self.splashPage = QWidget()
        self.splashPage.setObjectName(u"splashPage")
        self.splashPage.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.splashPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splashVerticalWidget = QWidget(self.splashPage)
        self.splashVerticalWidget.setObjectName(u"splashVerticalWidget")
        self.splashVerticalWidget.setAcceptDrops(True)
        self.splashVerticalWidget.setStyleSheet(u"/*This setting with override the style sheet. If you intend on creating a different style for this such as a light theme then I recommend that you remove this style.*/\n"
"QWidget{\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(30, 30, 30, 255), stop:1 rgba(60, 60, 60, 255));\n"
"}")
        self.verticalLayout = QVBoxLayout(self.splashVerticalWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.Logo = QLabel(self.splashVerticalWidget)
        self.Logo.setObjectName(u"Logo")
        sizePolicy3.setHeightForWidth(self.Logo.sizePolicy().hasHeightForWidth())
        self.Logo.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setFamilies([u"Montserrat 13"])
        font.setBold(True)
        font.setUnderline(True)
        self.Logo.setFont(font)
        self.Logo.setStyleSheet(u"background: transparent")
        self.Logo.setPixmap(QPixmap(u":/assets/images/remove_background_200_zoom.png"))
        self.Logo.setScaledContents(False)
        self.Logo.setMargin(0)

        self.verticalLayout.addWidget(self.Logo, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignBottom)

        self.subTitle = QLabel(self.splashVerticalWidget)
        self.subTitle.setObjectName(u"subTitle")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setWeight(QFont.Thin)
        font1.setKerning(True)
        self.subTitle.setFont(font1)
        self.subTitle.setAutoFillBackground(False)
        self.subTitle.setStyleSheet(u"QLabel {\n"
"  background-color: transparent;\n"
"  color: red;\n"
"  font-family: Montserrat;\n"
"  font-size: 24px;\n"
"  letter-spacing: 15px;\n"
"}")
        self.subTitle.setTextFormat(Qt.TextFormat.AutoText)

        self.verticalLayout.addWidget(self.subTitle, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)


        self.verticalLayout_3.addWidget(self.splashVerticalWidget)

        self.stackedWidget.addWidget(self.splashPage)
        self.summaryPage = QWidget()
        self.summaryPage.setObjectName(u"summaryPage")
        self.verticalLayout_4 = QVBoxLayout(self.summaryPage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget = QTabWidget(self.summaryPage)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setEnabled(False)
        self.tab.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.stackedWidget.addWidget(self.summaryPage)
        self.subgraphPage = QWidget()
        self.subgraphPage.setObjectName(u"subgraphPage")
        self.verticalLayout_37 = QVBoxLayout(self.subgraphPage)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.widget_2 = QWidget(self.subgraphPage)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy3.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy3)
        self.widget_2.setStyleSheet(u"")
        self.verticalLayout_10 = QVBoxLayout(self.widget_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.subgraphIcon = QLabel(self.widget_2)
        self.subgraphIcon.setObjectName(u"subgraphIcon")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.subgraphIcon.sizePolicy().hasHeightForWidth())
        self.subgraphIcon.setSizePolicy(sizePolicy4)
        self.subgraphIcon.setPixmap(QPixmap(u":/assets/icons/subgraph.png"))

        self.verticalLayout_10.addWidget(self.subgraphIcon, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignBottom)

        self.comingSoonLabel = QLabel(self.widget_2)
        self.comingSoonLabel.setObjectName(u"comingSoonLabel")

        self.verticalLayout_10.addWidget(self.comingSoonLabel, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_37.addWidget(self.widget_2)

        self.stackedWidget.addWidget(self.subgraphPage)

        self.verticalLayout_13.addWidget(self.stackedWidget)


        self.horizontalLayout_5.addWidget(self.appContentArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.exitBtn.clicked.connect(MainWindow.close)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"DigestAI", None))
#if QT_CONFIG(tooltip)
        self.openFileBtn.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Open (Ctrl-O)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.openFileBtn.setText("")
#if QT_CONFIG(shortcut)
        self.openFileBtn.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.openFolderBtn.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Multi-Model Analysis</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.openFolderBtn.setText("")
#if QT_CONFIG(tooltip)
        self.huggingfaceBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Huggingface", None))
#endif // QT_CONFIG(tooltip)
        self.huggingfaceBtn.setText("")
#if QT_CONFIG(tooltip)
        self.summaryBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Summary", None))
#endif // QT_CONFIG(tooltip)
        self.summaryBtn.setText("")
#if QT_CONFIG(tooltip)
        self.saveBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Save Report (Ctrl-S)", None))
#endif // QT_CONFIG(tooltip)
        self.saveBtn.setText("")
#if QT_CONFIG(shortcut)
        self.saveBtn.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.nodesListBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Node List", None))
#endif // QT_CONFIG(tooltip)
        self.nodesListBtn.setText("")
#if QT_CONFIG(shortcut)
        self.nodesListBtn.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.subgraphBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Subgraph", None))
#endif // QT_CONFIG(tooltip)
        self.subgraphBtn.setText("")
#if QT_CONFIG(tooltip)
        self.infoBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Info", None))
#endif // QT_CONFIG(tooltip)
        self.infoBtn.setText("")
#if QT_CONFIG(tooltip)
        self.exitBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Exit", None))
#endif // QT_CONFIG(tooltip)
        self.exitBtn.setText("")
        self.Logo.setText("")
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.subgraphIcon.setText("")
        self.comingSoonLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:20pt; font-style:italic;\">Coming soon...</span></p></body></html>", None))
    # retranslateUi

