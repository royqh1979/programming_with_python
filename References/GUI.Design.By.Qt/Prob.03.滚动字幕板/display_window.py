# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(666, 174)
        self.lblDisplay = QtWidgets.QLabel(Dialog)
        self.lblDisplay.setGeometry(QtCore.QRect(100, 60, 72, 15))
        self.lblDisplay.setText("")
        self.lblDisplay.setObjectName("lblDisplay")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "显示屏"))

