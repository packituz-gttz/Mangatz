# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MangaDownloader.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(718, 553)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushbutton_stop = QtGui.QPushButton(self.centralwidget)
        self.pushbutton_stop.setObjectName(_fromUtf8("pushbutton_stop"))
        self.horizontalLayout_3.addWidget(self.pushbutton_stop)
        self.pushbutton_start = QtGui.QPushButton(self.centralwidget)
        self.pushbutton_start.setObjectName(_fromUtf8("pushbutton_start"))
        self.horizontalLayout_3.addWidget(self.pushbutton_start)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.edit_url = QtGui.QLineEdit(self.centralwidget)
        self.edit_url.setObjectName(_fromUtf8("edit_url"))
        self.horizontalLayout_2.addWidget(self.edit_url)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.series_title_label = QtGui.QLabel(self.centralwidget)
        self.series_title_label.setStyleSheet(_fromUtf8("color: rgb(85, 170, 255);\n"
"font: 75 16pt \"Cantarell\";\n"
""))
        self.series_title_label.setText(_fromUtf8(""))
        self.series_title_label.setObjectName(_fromUtf8("series_title_label"))
        self.verticalLayout_2.addWidget(self.series_title_label)
        self.label_image = QtGui.QLabel(self.centralwidget)
        self.label_image.setMinimumSize(QtCore.QSize(200, 200))
        self.label_image.setText(_fromUtf8(""))
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setObjectName(_fromUtf8("label_image"))
        self.verticalLayout_2.addWidget(self.label_image)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.progressbar_download = QtGui.QProgressBar(self.centralwidget)
        self.progressbar_download.setProperty("value", 0)
        self.progressbar_download.setObjectName(_fromUtf8("progressbar_download"))
        self.gridLayout.addWidget(self.progressbar_download, 3, 0, 1, 1)
        self.label_chapter = QtGui.QLabel(self.centralwidget)
        self.label_chapter.setStyleSheet(_fromUtf8("color: rgb(85, 170, 255);\n"
"font: 14pt \"Cantarell\";"))
        self.label_chapter.setText(_fromUtf8(""))
        self.label_chapter.setObjectName(_fromUtf8("label_chapter"))
        self.gridLayout.addWidget(self.label_chapter, 1, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 718, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Recent = QtGui.QMenu(self.menuFile)
        self.menu_Recent.setObjectName(_fromUtf8("menu_Recent"))
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName(_fromUtf8("menu_Edit"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionMangatz_Help = QtGui.QAction(MainWindow)
        self.actionMangatz_Help.setObjectName(_fromUtf8("actionMangatz_Help"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionMe = QtGui.QAction(MainWindow)
        self.actionMe.setObjectName(_fromUtf8("actionMe"))
        self.menuFile.addAction(self.menu_Recent.menuAction())
        self.menuFile.addAction(self.action_Quit)
        self.menu_Edit.addAction(self.actionPreferences)
        self.menu_Help.addAction(self.actionMangatz_Help)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.label.setBuddy(self.edit_url)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Mangatz", None))
        self.pushbutton_stop.setText(_translate("MainWindow", "Sto&p", None))
        self.pushbutton_start.setText(_translate("MainWindow", "&Start", None))
        self.label.setText(_translate("MainWindow", "&URL:", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menu_Recent.setTitle(_translate("MainWindow", "&Recent", None))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit", None))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionMangatz_Help.setText(_translate("MainWindow", "Mangatz &Help", None))
        self.action_Quit.setText(_translate("MainWindow", "&Quit", None))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences...", None))
        self.actionMe.setText(_translate("MainWindow", "me", None))

