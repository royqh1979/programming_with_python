# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'equal_total_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 185)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txtRatio = QtWidgets.QLineEdit(Dialog)
        self.txtRatio.setReadOnly(True)
        self.txtRatio.setObjectName("txtRatio")
        self.gridLayout.addWidget(self.txtRatio, 2, 1, 1, 1)
        self.txtEachMonth = QtWidgets.QLineEdit(Dialog)
        self.txtEachMonth.setReadOnly(True)
        self.txtEachMonth.setObjectName("txtEachMonth")
        self.gridLayout.addWidget(self.txtEachMonth, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txtTotal = QtWidgets.QLineEdit(Dialog)
        self.txtTotal.setText("")
        self.txtTotal.setReadOnly(True)
        self.txtTotal.setObjectName("txtTotal")
        self.gridLayout.addWidget(self.txtTotal, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "等额本息还款法"))
        self.label_3.setText(_translate("Dialog", "还款与贷款之比"))
        self.label.setText(_translate("Dialog", "每月还款额（元）"))
        self.label_2.setText(_translate("Dialog", "全部本息总和（元）"))
        self.pushButton.setText(_translate("Dialog", "关闭"))

