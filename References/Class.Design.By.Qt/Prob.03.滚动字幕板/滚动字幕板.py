from dataclasses import dataclass
from typing import List

from display_window import Ui_Dialog as DisplayWindowUi
from control_panel import Ui_Dialog as ControlPanelUi
from PyQt5 import QtWidgets, QtCore, QtGui


@dataclass
class Color:
    name:str
    value:QtGui.QColor

colors = [
    Color('黑色','black'),
    Color('绿色', 'green'),
    Color('蓝色', 'blue'),
    Color('青色', 'cyan'),
    Color('红色', 'red'),
    Color('黄色', 'yellow'),
    Color('紫色', 'purple'),
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

    def on_time_out(self):
        if self._rolling:
            lblDisplay = self.display_window.ui.lblDisplay
            lblDisplay.move(lblDisplay.x()-1,lblDisplay.y())

    def toggle_rolling(self):
        if self._rolling:
            self._rolling = False
            self._timer.stop()
        else:
            self._rolling = True
            lblDisplay = self.display_window.ui.lblDisplay
            font = lblDisplay.font()

            if self.ui.rdBigFont.isChecked():
                font.setPixelSize(40)
            else:
                font.setPixelSize(28)

            for i in range(len(font_names)):
                if self.font_name_btns[i].isChecked():
                    font.setFamily(font_names[i])

            lblDisplay.setFont(font)
            for i in range(len(txts)):
                if self.txt_btns[i].isChecked():
                    lblDisplay.setText(txts[i])
                    break
            else:
                lblDisplay.setText(self.ui.txtCustom.text())
            fore_color = self.ui.cbForeground.itemData(self.ui.cbForeground.currentIndex())
            back_color = self.ui.cbBackground.itemData(self.ui.cbBackground.currentIndex())

            print(fore_color,back_color)

            lblDisplay.setStyleSheet(f"QLabel {{ color: {fore_color}; background-color: {back_color}; }}")
            self.display_window.setStyleSheet(f"QWidget {{background-color: {back_color}; }}")
            size=lblDisplay.sizeHint()
            lblDisplay.setMinimumSize(size.width(),size.height())
            self._timer.start(50)




if __name__=='__main__':
    app = QtWidgets.QApplication([])
    display_window = DisplayWindow()
    control_panel = ControlPanel(display_window)
    display_window.show()
    control_panel.show()
    app.exec()
