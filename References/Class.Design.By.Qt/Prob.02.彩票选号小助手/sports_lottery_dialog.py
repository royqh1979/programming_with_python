from time import sleep
from typing import List

from PyQt5.QtCore import QThread

from sports_lottery_dlg import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
import random


class SportsLotteryDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 从GridLayout的各单元格中取出对应的文本框控件，并保存在btn_numbers和btn_special_numbers列表中
        self.btn_numbers:List[List[QtWidgets.QPushButton]]=[] # 5行6列，共30个文本框
        self.btn_special_numbers:List[QtWidgets.QPushButton]=[] # 5行1列，共1个文本框

        for i in range(self.ui.grpNumbersLayout.rowCount()):
            numbers = []
            for j in range(6):
                item = self.ui.grpNumbersLayout.itemAtPosition(i,j)
                btn_number:QtWidgets.QPushButton = item.widget()
                btn_number.setProperty("data_row",i)
                btn_number.setStyleSheet("QPushButton{background-color: pink; font-size:28px; "
                                         "font-weight: bold; border: 2px groove gray; border-style:inset;}")
                btn_number.clicked.connect(self.on_btn_number_clicked)
                numbers.append(btn_number)
            self.btn_numbers.append(numbers)
            item = self.ui.grpNumbersLayout.itemAtPosition(i,7)
            btn_special_number:QtWidgets.QPushButton = item.widget()
            btn_special_number.setProperty("data_row",i)
            btn_special_number.setStyleSheet(
                "QPushButton{background-color: DarkSeaGreen; font-size:28px; font-weight: bold; "
                "border: 2px groove gray; border-style:inset;}")

            btn_special_number.clicked.connect(self.on_btn_special_number_clicked)
            self.btn_special_numbers.append(btn_special_number)

        # 从VBoxLayout的各行中取出对应的单选按钮控件，并保存在radio_bets列中中
        self.radio_bets:List[QtWidgets.QRadioButton]=[]
        for i in range(self.ui.grpBetsLayout.count()):
            item = self.ui.grpBetsLayout.itemAt(i)
            radio_bet: QtWidgets.QRadioButton= item.widget()
            radio_bet.clicked.connect(self.on_bet_select)
            radio_bet.setProperty("data_row",i)
            self.radio_bets.append(radio_bet)


        self.current_row = 0
        self.radio_bets[self.current_row].setChecked(True)

        self.timer = QtCore.QTimer(self)
        self.ui.btnStart.clicked.connect(self.on_start_gen_numbers)
        self.ui.btnStop.clicked.connect(self.on_stop_gen_numbers)



    def on_bet_select(self):
        radio_bet = self.sender()
        row = radio_bet.property("data_row")
        print(row)

    def on_btn_number_clicked(self):
        btn_number : QtWidgets.QPushButton = self.sender()
        row = btn_number.property("data_row")
        self.radio_bets[row].setChecked(True)
        self.current_row=row
        gen_rand_digit(btn_number,9)

    def on_btn_special_number_clicked(self):
        btn_special_number : QtWidgets.QPushButton = self.sender()
        row = btn_special_number.property("data_row")
        self.radio_bets[row].setChecked(True)
        self.current_row=row
        gen_rand_digit(btn_special_number,4)

    def on_start_gen_numbers(self):
        self.timer.timeout.connect(self.on_generating)
        self.timer.start(20)

    def on_generating(self):
        for i in range(len(self.btn_numbers[self.current_row])):
            btn_number : QtWidgets.QPushButton = self.btn_numbers[self.current_row][i]
            btn_number.setText(str(random.randint(0, 9)))
        btn_special_number : QtWidgets.QPushButton = self.btn_special_numbers[self.current_row]
        btn_special_number.setText(str(random.randint(0, 4)))

    def on_stop_gen_numbers(self):
        self.timer.stop()
        self.timer.timeout.disconnect(self.on_generating)

def gen_rand_digit(btn:QtWidgets.QPushButton, max_value:int):
    for i in range(10):
        btn.setText(str(random.randint(0, max_value)))
        btn.repaint()
        QThread.msleep(20)







random.seed()