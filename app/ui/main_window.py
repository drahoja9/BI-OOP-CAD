# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 811)
        self.mainArea = QtWidgets.QWidget(MainWindow)
        self.mainArea.setObjectName("mainArea")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainArea)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.mainArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 949, 547))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.textBrowser = QtWidgets.QTextBrowser(self.mainArea)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser, 0, QtCore.Qt.AlignBottom)
        MainWindow.setCentralWidget(self.mainArea)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1047, 28))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCommands = QtWidgets.QMenu(self.menubar)
        self.menuCommands.setObjectName("menuCommands")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionLine = QtWidgets.QAction(MainWindow)
        self.actionLine.setObjectName("actionLine")
        self.actionRectangle = QtWidgets.QAction(MainWindow)
        self.actionRectangle.setObjectName("actionRectangle")
        self.actionCircle = QtWidgets.QAction(MainWindow)
        self.actionCircle.setObjectName("actionCircle")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCommands.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionLine)
        self.toolBar.addAction(self.actionRectangle)
        self.toolBar.addAction(self.actionCircle)

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.hide)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuCommands.setTitle(_translate("MainWindow", "&Commands"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "&New"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionLine.setText(_translate("MainWindow", "Line"))
        self.actionRectangle.setText(_translate("MainWindow", "Rectangle"))
        self.actionCircle.setText(_translate("MainWindow", "Circle"))

