# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'front_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(661, 542)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(36)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources/face.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnSportLottery = QtWidgets.QPushButton(self.frame)
        self.btnSportLottery.setObjectName("btnSportLottery")
        self.horizontalLayout_2.addWidget(self.btnSportLottery)
        self.btnWelfareLottery = QtWidgets.QPushButton(self.frame)
        self.btnWelfareLottery.setObjectName("btnWelfareLottery")
        self.horizontalLayout_2.addWidget(self.btnWelfareLottery)
        self.btnExit = QtWidgets.QPushButton(self.frame)
        self.btnExit.setObjectName("btnExit")
        self.horizontalLayout_2.addWidget(self.btnExit)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        self.btnExit.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "彩票选号小助手"))
        self.label_2.setText(_translate("Dialog", "彩票选号小助手"))
        self.btnSportLottery.setText(_translate("Dialog", "体育彩票"))
        self.btnWelfareLottery.setText(_translate("Dialog", "福利彩票"))
        self.btnExit.setText(_translate("Dialog", "退出"))

