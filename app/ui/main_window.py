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
        MainWindow.resize(1134, 601)
        self.mainArea = QtWidgets.QWidget(MainWindow)
        self.mainArea.setObjectName("mainArea")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.mainArea)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.brushes = QtWidgets.QVBoxLayout()
        self.brushes.setSpacing(0)
        self.brushes.setObjectName("brushes")
        self.dotButton = QtWidgets.QPushButton(self.mainArea)
        self.dotButton.setObjectName("dotButton")
        self.brushes.addWidget(self.dotButton)
        self.lineButton = QtWidgets.QPushButton(self.mainArea)
        self.lineButton.setObjectName("lineButton")
        self.brushes.addWidget(self.lineButton)
        self.polylineButton = QtWidgets.QPushButton(self.mainArea)
        self.polylineButton.setObjectName("polylineButton")
        self.brushes.addWidget(self.polylineButton)
        self.circleButton = QtWidgets.QPushButton(self.mainArea)
        self.circleButton.setObjectName("circleButton")
        self.brushes.addWidget(self.circleButton)
        self.rectagleButton = QtWidgets.QPushButton(self.mainArea)
        self.rectagleButton.setEnabled(True)
        self.rectagleButton.setObjectName("rectagleButton")
        self.brushes.addWidget(self.rectagleButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.brushes.addItem(spacerItem)
        self.colorButton = QtWidgets.QPushButton(self.mainArea)
        self.colorButton.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.colorButton.setFlat(False)
        self.colorButton.setObjectName("colorButton")
        self.brushes.addWidget(self.colorButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.brushes.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.brushes)
        self.canvasAndInput = QtWidgets.QVBoxLayout()
        self.canvasAndInput.setContentsMargins(0, -1, -1, -1)
        self.canvasAndInput.setObjectName("canvasAndInput")
        self.splitter = QtWidgets.QSplitter(self.mainArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(0, 0))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(2)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.canvasHolder = QtWidgets.QScrollArea(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvasHolder.sizePolicy().hasHeightForWidth())
        self.canvasHolder.setSizePolicy(sizePolicy)
        self.canvasHolder.setMinimumSize(QtCore.QSize(0, 400))
        self.canvasHolder.setBaseSize(QtCore.QSize(0, 0))
        self.canvasHolder.setWidgetResizable(True)
        self.canvasHolder.setObjectName("canvasHolder")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1023, 396))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.canvasHolder.setWidget(self.scrollAreaWidgetContents)
        self.textBrowser = QtWidgets.QTextBrowser(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 40))
        self.textBrowser.setObjectName("textBrowser")
        self.canvasAndInput.addWidget(self.splitter)
        self.horizontalLayout.addLayout(self.canvasAndInput)
        MainWindow.setCentralWidget(self.mainArea)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1134, 28))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OOP CAD"))
        self.dotButton.setText(_translate("MainWindow", "Dot"))
        self.lineButton.setText(_translate("MainWindow", "Line"))
        self.polylineButton.setText(_translate("MainWindow", "Polyline"))
        self.circleButton.setText(_translate("MainWindow", "Circle"))
        self.rectagleButton.setText(_translate("MainWindow", "Rectangle"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuEdit.setTitle(_translate("MainWindow", "E&dit"))
        self.actionNew.setText(_translate("MainWindow", "&New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionLine.setText(_translate("MainWindow", "Line"))
        self.actionRectangle.setText(_translate("MainWindow", "Rectangle"))
        self.actionCircle.setText(_translate("MainWindow", "Circle"))
        self.actionUndo.setText(_translate("MainWindow", "&Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "&Redo"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))

