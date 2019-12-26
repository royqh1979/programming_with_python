# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(918, 840)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_view = MainGraphicsView(Form)
        self.main_view.setObjectName("main_view")
        self.verticalLayout.addWidget(self.main_view)
        self.line = QtWidgets.QFrame(Form)
        self.line.setMinimumSize(QtCore.QSize(0, 2))
        self.line.setStyleSheet("")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.formLayout = QtWidgets.QFormLayout(self.frame_2)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cbDifficulty = QtWidgets.QComboBox(self.frame_2)
        self.cbDifficulty.setObjectName("cbDifficulty")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbDifficulty)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txtScore = QtWidgets.QLineEdit(self.frame_2)
        self.txtScore.setReadOnly(True)
        self.txtScore.setObjectName("txtScore")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtScore)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.horizontalLayout.addWidget(self.frame_2)
        self.point_frame = ArrowFrame(self.frame)
        self.point_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.point_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.point_frame.setObjectName("point_frame")
        self.horizontalLayout.addWidget(self.point_frame)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.formLayout_2 = QtWidgets.QFormLayout(self.frame_4)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txtTime = QtWidgets.QLineEdit(self.frame_4)
        self.txtTime.setReadOnly(True)
        self.txtTime.setObjectName("txtTime")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtTime)
        self.txtLife = QtWidgets.QLineEdit(self.frame_4)
        self.txtLife.setReadOnly(True)
        self.txtLife.setObjectName("txtLife")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtLife)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.horizontalLayout.addWidget(self.frame_4)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "打冰雹游戏"))
        self.label.setText(_translate("Form", "选择难度"))
        self.label_2.setText(_translate("Form", "得分"))
        self.label_3.setText(_translate("Form", "剩余能量"))
        self.label_4.setText(_translate("Form", "所用时间"))
from arrow_frame import ArrowFrame
from main_graphicsview import MainGraphicsView
