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


        self.current_row = 0 #当前被选中的行号
        self.radio_bets[self.current_row].setChecked(True)

        self.timer = QtCore.QTimer(self)
        self.ui.btnStart.clicked.connect(self.on_start_gen_numbers)
        self.ui.btnStop.clicked.connect(self.on_stop_gen_numbers)
        self.ui.btnAutoGenerate.clicked.connect(self.on_start_gen_all_numbers)
        self.ui.btnReturn.clicked.connect(self.close)
        self.ui.btnStop.setEnabled(False)



    def on_bet_select(self):
        """
        处理单选钮被选中事件
        """
        radio_bet = self.sender()
        self.current_row = radio_bet.property("data_row")

    def on_btn_number_clicked(self):
        """
        处理单个数字框被点击事件
        """
        btn_number : QtWidgets.QPushButton = self.sender()
        row = btn_number.property("data_row")
        self.radio_bets[row].setChecked(True)
        self.current_row=row
        gen_rand_digit(btn_number,9)

    def on_btn_special_number_clicked(self):
        """
        处理单个（特殊）数字框被点击事件
        """
        btn_special_number : QtWidgets.QPushButton = self.sender()
        row = btn_special_number.property("data_row")
        self.radio_bets[row].setChecked(True)
        self.current_row=row
        gen_rand_digit(btn_special_number,4)

    def on_start_gen_all_numbers(self)->None:
        """
        开始逐行生成随机数字

        """
        self.ui.btnStop.setEnabled(False)
        self.ui.btnStart.setEnabled(False)
        self.ui.btnAutoGenerate.setEnabled(False)
        self.timer.setProperty("data_count",0)
        self.timer.setProperty("data_row",0)
        self.timer.timeout.connect(self.on_generating_all)
        self.timer.start(20)

    def on_generating_all(self)->None:
        """
        定时逐行生成随机数字
        """
        count=self.timer.property("data_count")
        row = self.timer.property("data_row")
        for i in range(len(self.btn_numbers[row])):
            btn_number : QtWidgets.QPushButton = self.btn_numbers[row][i]
            btn_number.setText(str(random.randint(0, 9)))
        btn_special_number : QtWidgets.QPushButton = self.btn_special_numbers[row]
        btn_special_number.setText(str(random.randint(0, 4)))
        count+=1
        if count>10:
            count=0
            row+=1
            print(count,row)
            if row>=len(self.btn_special_numbers):
                self.timer.stop()
                self.timer.timeout.disconnect(self.on_generating_all)
                self.ui.btnStop.setEnabled(False)
                self.ui.btnStart.setEnabled(True)
                self.ui.btnAutoGenerate.setEnabled(True)
                return
        self.timer.setProperty("data_count",count)
        self.timer.setProperty("data_row",row)


    def on_start_gen_numbers(self)->None:
        """
        开始在一行上生成随机数字（开始按钮被点击）
        """
        self.timer.timeout.connect(self.on_generating)
        self.timer.start(20)
        self.ui.btnStop.setEnabled(True)
        self.ui.btnStart.setEnabled(False)
        self.ui.btnAutoGenerate.setEnabled(False)

    def on_generating(self)->None:
        """
        定时在一行上生成随机数字
        """
        for i in range(len(self.btn_numbers[self.current_row])):
            btn_number : QtWidgets.QPushButton = self.btn_numbers[self.current_row][i]
            btn_number.setText(str(random.randint(0, 9)))
        btn_special_number : QtWidgets.QPushButton = self.btn_special_numbers[self.current_row]
        btn_special_number.setText(str(random.randint(0, 4)))

    def on_stop_gen_numbers(self)->None:
        """
        停止在一行上生成随机数字（停止按钮被点击）
        """
        self.timer.stop()
        self.timer.timeout.disconnect(self.on_generating)
        self.ui.btnStop.setEnabled(False)
        self.ui.btnStart.setEnabled(True)
        self.ui.btnAutoGenerate.setEnabled(True)


def gen_rand_digit(btn:QtWidgets.QPushButton, max_value:int):
    for i in range(10):
        btn.setText(str(random.randint(0, max_value)))
        btn.repaint()
        QThread.msleep(20)







random.seed()