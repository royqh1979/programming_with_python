from typing import List

from sports_lottery_dlg import Ui_Dialog
from PyQt5 import QtWidgets
import random


class SportsLotteryDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 从GridLayout的各单元格中取出对应的文本框控件，并保存在txt_numbers和txt_special_numbers列表中
        self.txt_numbers:List[List[QtWidgets.QTextEdit]]=[] # 5行6列，共30个文本框
        self.txt_special_numbers:List[QtWidgets.QTextEdit]=[] # 5行1列，共1个文本框

        for i in range(self.ui.grpNumbersLayout.rowCount()):
            numbers = []
            for j in range(6):
                item = self.ui.grpNumbersLayout.itemAtPosition(i,j)
                txt_number = item.widget()
                txt_number.setProperty("data_row",i)
                txt_number.setProperty("data_col",j)
                numbers.append(txt_number)
            self.txt_numbers.append(numbers)
            item = self.ui.grpNumbersLayout.itemAtPosition(i,7)
            self.txt_special_numbers.append(item.widget())

        # 从VBoxLayout的各行中取出对应的单选按钮控件，并保存在radio_bets列中中
        self.radio_bets:List[QtWidgets.QRadioButton]=[]
        for i in range(self.ui.grpBetsLayout.count()):
            item = self.ui.grpBetsLayout.itemAt(i)
            radio_bet: QtWidgets.QRadioButton= item.widget()
            radio_bet.clicked.connect(self.on_bet_select)
            radio_bet.setProperty("data_row",i)
            self.radio_bets.append(radio_bet)


        self.current_row = 0

    def on_bet_select(self):
        radio_bet = self.sender()
        row = radio_bet.property("data_row")
        print(row)

    def on_txt_clicked(self):
        txt_number = self.sender()
        row = txt_number.property("data_row")
        col = txt_number.property("data_col")



random.seed()