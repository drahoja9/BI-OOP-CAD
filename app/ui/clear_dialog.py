# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './app/ui/clear_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_clearDialog(object):
    def setupUi(self, clearDialog):
        clearDialog.setObjectName("clearDialog")
        clearDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        clearDialog.resize(410, 88)
        clearDialog.setModal(True)
        self.clearButtonBox = QtWidgets.QDialogButtonBox(clearDialog)
        self.clearButtonBox.setGeometry(QtCore.QRect(110, 40, 181, 32))
        self.clearButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.clearButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.clearButtonBox.setObjectName("clearButtonBox")
        self.clearMessage = QtWidgets.QLabel(clearDialog)
        self.clearMessage.setGeometry(QtCore.QRect(40, 10, 341, 21))
        self.clearMessage.setObjectName("clearMessage")

        self.retranslateUi(clearDialog)
        self.clearButtonBox.accepted.connect(clearDialog.accept)
        self.clearButtonBox.rejected.connect(clearDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(clearDialog)

    def retranslateUi(self, clearDialog):
        _translate = QtCore.QCoreApplication.translate
        clearDialog.setWindowTitle(_translate("clearDialog", "Are you sure?"))
        self.clearMessage.setText(_translate("clearDialog", "Are you sure you want to clear the whole canvas?"))

