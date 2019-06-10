from dataclasses import dataclass
from typing import List

from display_window import Ui_Dialog as DisplayWindowUi
from control_panel import Ui_Dialog as ControlPanelUi
from PyQt5 import QtWidgets, QtCore, QtGui

import random


@dataclass
class Color:
    name:str
    value:str
    contrast_color: str

colors = [
    Color('黑色','black','white'),
    Color('绿色', 'green','purple'),
    Color('蓝色', 'blue','yellow'),
    Color('青色', 'cyan','red'),
    Color('红色', 'red','cyan'),
    Color('黄色', 'yellow','blue'),
    Color('紫色', 'purple','cyan'),
]


font_names = [
    "宋体",
    "隶书",
    "楷体",
    "黑体"
]
txts = [
    '北京方向的66次列车就要开车了',
    '神州飞船，载誉归来！',
    '东方明珠，开盘价20元/股',
    '宝剑锋从磨砺出，梅花香自苦寒来',
    '欲穷千里目，更上一层楼',
    'No Pain, No Gain',
    '书山有路勤为径，学海无涯苦作舟',
    '团结起来，共同战胜“非典”'
]

class DisplayWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__();
        self.ui=DisplayWindowUi()
        self.ui.setupUi(self)
        #让窗口始终在最前
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        app.quit()

class ControlPanel(QtWidgets.QDialog):
    def __init__(self,display_window:DisplayWindow):
        super().__init__();
        self.display_window=display_window
        self.ui=ControlPanelUi()
        self.ui.setupUi(self)

        for c in colors:
            self.ui.cbBackground.addItem(c.name,c.value)
            self.ui.cbForeground.addItem(c.name,c.value)

        self.ui.cbBackground.setCurrentText("绿色")
        self.ui.cbForeground.setCurrentText("紫色")

        #获取全部文字选择按钮
        self.txt_btns:List[QtWidgets.QPushButton] = []
        for i in range(self.ui.txt_btn_layout.rowCount()):
            for j in range(self.ui.txt_btn_layout.columnCount()):
                self.txt_btns.append(self.ui.txt_btn_layout.itemAtPosition(i,j).widget())

        #获取全部字体名称按钮
        self.font_name_btns:List[QtWidgets.QPushButton] = []
        for i in range(self.ui.font_name_layout.count()):
            self.font_name_btns.append(self.ui.font_name_layout.itemAt(i).widget())

        # todo: 滚动方向


        self.ui.btnExit.clicked.connect(app.quit)
        self.ui.btnHide.clicked.connect(self.hide)
        self._rolling = False
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.on_time_out)
        self.ui.btnStart.clicked.connect(self.toggle_rolling)
        self.ui.txtCustom.returnPressed.connect(self.clear_txt_selection)

        self.ui.sldSpeed.setRange(1,20)
        self.ui.sldSpeed.valueChanged.connect(self.set_speed)
        self.ui.sldSpeed.setValue(1)
        self._speed=1
        self._orient_left = True

        self.ui.cbChangeColor.stateChanged.connect(self.set_change_color)
        self._frame_count = 0

    def set_change_color(self):
        #如果打开“自动改变颜色”，则禁用前景色和背景色选择
        enable_color = not self.ui.cbChangeColor.isChecked()
        self.ui.cbBackground.setEnabled(enable_color)
        self.ui.cbForeground.setEnabled(enable_color)

    def set_speed(self,speed):
        self._speed = speed

    def clear_txt_selection(self):
        for btn in self.txt_btns:
            btn.setChecked(False)

    def on_time_out(self):
        if not self._rolling:
            return
        lblDisplay = self.display_window.ui.lblDisplay
        x=lblDisplay.x()
        y=lblDisplay.y()
        if self.ui.rdOrientLeft.isChecked():
            self._orient_left = True
            if lblDisplay.x()+lblDisplay.width() < 0:
                x=self.display_window.width()
            else:
                x=lblDisplay.x()-self._speed
        elif self.ui.rdOrientRight.isChecked():
            self._orient_left = False
            if lblDisplay.x() > self.display_window.width():
                x=-lblDisplay.width()
            else:
                x=lblDisplay.x()+self._speed
        elif self.ui.rdSwing.isChecked():
            if self._orient_left:
                if lblDisplay.x() + lblDisplay.width() < 0:
                    self._orient_left = False
                else:
                    x = lblDisplay.x() - self._speed
            else:
                if lblDisplay.x() > self.display_window.width():
                    self._orient_left = True
                else:
                    x = lblDisplay.x() + self._speed
        else:
            if self._orient_left:
                if lblDisplay.x() <= 0:
                    self._orient_left = False
                else:
                    x = lblDisplay.x() - self._speed
            else:
                if lblDisplay.x()+lblDisplay.width() >= self.display_window.width():
                    self._orient_left = True
                else:
                    x = lblDisplay.x() + self._speed

        lblDisplay.move(x,y)
        if self._frame_count==0:
            if self.ui.cbChangeColor.isChecked():
                color = random.choice(colors)
                lblDisplay.setStyleSheet(f"QLabel {{ color: {color.value}; background-color: {color.contrast_color}; }}")
                self.display_window.setStyleSheet(f"QWidget {{background-color: {color.contrast_color}; }}")
        self._frame_count += 1
        if self._frame_count > 30:
            self._frame_count = 0


    def toggle_rolling(self):
        if self._rolling:
            self._rolling = False
            self._timer.stop()
            self.ui.btnStart.setText("开始滚动")
        else:
            self._rolling = True
            self.ui.btnStart.setText("停止滚动")
            lblDisplay = self.display_window.ui.lblDisplay
            font = lblDisplay.font()

            # 字体大小
            if self.ui.rdBigFont.isChecked():
                font.setPixelSize(40)
            else:
                font.setPixelSize(28)

            #字体名称
            for i in range(len(font_names)):
                if self.font_name_btns[i].isChecked():
                    font.setFamily(font_names[i])

            lblDisplay.setFont(font)
            # 文字内容
            for i in range(len(txts)):
                if self.txt_btns[i].isChecked():
                    lblDisplay.setText(txts[i])
                    break
            else:
                lblDisplay.setText(self.ui.txtCustom.text())

            # 文字颜色
            if not self.ui.cbChangeColor.isChecked():
                fore_color = self.ui.cbForeground.itemData(self.ui.cbForeground.currentIndex())
                back_color = self.ui.cbBackground.itemData(self.ui.cbBackground.currentIndex())
                lblDisplay.setStyleSheet(f"QLabel {{ color: {fore_color}; background-color: {back_color}; }}")
                self.display_window.setStyleSheet(f"QWidget {{background-color: {back_color}; }}")

            # 重新设置滚动标签大小（以便完整显示所有文字）
            size=lblDisplay.sizeHint()
            lblDisplay.setMinimumSize(size.width(),size.height())
            self._timer.start(50)


if __name__=='__main__':
    random.seed()
    app = QtWidgets.QApplication([])
    display_window = DisplayWindow()
    control_panel = ControlPanel(display_window)
    display_window.show()
    control_panel.show()
    app.exec()
