from time import sleep
from typing import List

from PyQt5.QtCore import QThread

from welfare_lottery_dlg import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
import random


class WelfareLotteryDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 从GridLayout的各单元格中取出对应的文本框控件，并保存在列表中
        self.btn_numbers:List[List[QtWidgets.QPushButton]]=[] # 5行7列，共35个文本框

        for i in range(self.ui.grpNumbersLayout.rowCount()):
            btn_numbers = []
            for j in range(self.ui.grpNumbersLayout.columnCount()):
                item = self.ui.grpNumbersLayout.itemAtPosition(i,j)
                btn_number: QtWidgets.QPushButton=item.widget()
                btn_number.setStyleSheet("QPushButton{background-color: pink; font-size:28px; "
                                         "font-weight: bold; border: 2px groove gray; border-style:inset;}")
                # 下面三行代码保证按钮被隐藏时，不会改变对话框的布局
                sp_retain = btn_number.sizePolicy()
                sp_retain.setRetainSizeWhenHidden(True)
                btn_number.setSizePolicy(sp_retain)

                btn_numbers.append(btn_number)
            self.btn_numbers.append(btn_numbers)

        # 从VBoxLayout的各行中取出对应的单选按钮控件，并保存在radio_bets列中中
        self.radio_bets:List[QtWidgets.QRadioButton]=[]
        for i in range(self.ui.grpBetsLayout.count()):
            item = self.ui.grpBetsLayout.itemAt(i)
            radio_bet:QtWidgets.QRadioButton = item.widget()
            radio_bet.setProperty("data_row",i)
            radio_bet.clicked.connect(self.on_radio_bet_checked)
            self.radio_bets.append(radio_bet)

        self.current_row = 4 #当前被选中的行号
        self.radio_bets[self.current_row].setChecked(True)
        self.ui.btnReturn.clicked.connect(self.close)
        self.ui.btnStart.clicked.connect(self.on_gen_numbers)
        self.ui.btnClear.clicked.connect(self.on_clear)

    def on_radio_bet_checked(self):
        radio_bet = self.sender()
        self.current_row = radio_bet.property("data_row")
        for i in range(len(self.btn_numbers)):
            for j in range(len(self.btn_numbers[i])):
                if i>self.current_row:
                    self.btn_numbers[i][j].hide()
                else:
                    self.btn_numbers[i][j].show()

    def on_clear(self):
        for i in range(len(self.btn_numbers)):
            for j in range(len(self.btn_numbers[i])):
                self.btn_numbers[i][j].setText("")

    def on_gen_numbers(self):
        for i in range(self.current_row+1):
            for j in range(len(self.btn_numbers[i])):
                num=random.randint(1,35)
                self.btn_numbers[i][j].setText(f"{num:02d}")
        QThread.msleep(50)

random.seed()