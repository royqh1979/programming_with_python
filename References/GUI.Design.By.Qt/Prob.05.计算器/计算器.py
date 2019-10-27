from decimal import Decimal

from main_window import Ui_Form as MainFormUI

from PyQt5 import QtWidgets,QtGui,QtCore

class MainFrame(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._ui=MainFormUI()
        self._ui.setupUi(self)
        self._value="0"
        self._last_value="0"
        self._op=""
        self._append_period = False
        # 数字键
        self._ui.btn1.clicked.connect(self.onBtn1Click)
        self._ui.btn2.clicked.connect(self.onBtn2Click)
        self._ui.btn3.clicked.connect(self.onBtn3Click)
        self._ui.btn4.clicked.connect(self.onBtn4Click)
        self._ui.btn5.clicked.connect(self.onBtn5Click)
        self._ui.btn6.clicked.connect(self.onBtn6Click)
        self._ui.btn7.clicked.connect(self.onBtn7Click)
        self._ui.btn8.clicked.connect(self.onBtn8Click)
        self._ui.btn9.clicked.connect(self.onBtn9Click)
        self._ui.btn0.clicked.connect(self.onBtn0Click)
        # 清除键
        self._ui.btnClear.clicked.connect(self.onBtnClearClick)
        self._ui.btnBackspace.clicked.connect(self.onBtnBackspaceClick)
        # 符号键
        self._ui.btnSign.clicked.connect(self.onBtnSignClick)
        # 小数点
        self._ui.btnPeriod.clicked.connect(self.onBtnPeriodClick)
        # 加减乘除
        self._ui.btnAdd.clicked.connect(self.onBtnAddClick)
        self._ui.btnMinus.clicked.connect(self.onBtnMinusClick)
        self._ui.btnMultiply.clicked.connect(self.onBtnMultiplyClick)
        self._ui.btnDivide.clicked.connect(self.onBtnDivideClick)
        self._ui.btnResult.clicked.connect(self.onBtnResultClick)


    def updateValue(self,value:str):
        self._value = value
        self._ui.displayFrame.setText(value)

    def appendDigit(self,digit):
        if self._op!="":
            self.clearCurrentValue()
            self.updateValue(digit)
            return
        if len(self._value)>=15:
            return
        if self._append_period:
            self._value += '.'
            self._append_period = False

        if self._value == '0' :
                self.updateValue(digit)
        else:
            self.updateValue(self._value+digit)

    def onBtn1Click(self):
        self.appendDigit("1")

    def onBtn2Click(self):
        self.appendDigit("2")

    def onBtn3Click(self):
        self.appendDigit("3")

    def onBtn4Click(self):
        self.appendDigit("4")

    def onBtn5Click(self):
        self.appendDigit("5")

    def onBtn6Click(self):
        self.appendDigit("6")

    def onBtn7Click(self):
        self.appendDigit("7")

    def onBtn8Click(self):
        self.appendDigit("8")

    def onBtn9Click(self):
        self.appendDigit("9")

    def onBtn0Click(self):
        self.appendDigit("0")

    def onBtnClearClick(self):
        self._last_value="0"
        self._op = ""
        self.clearCurrentValue()

    def clearCurrentValue(self):
        self._append_period = False
        self.updateValue("0")

    def onBtnBackspaceClick(self):
        if len(self._value)>1:
            self.updateValue(self._value[0:-1])
        else:
            self.clearCurrentValue()

    def onBtnSignClick(self):
        if self._value == '0':
            return
        if self._value[0]=='-':
            self.updateValue(self._value[1:])
        else:
            self.updateValue("+"+self._value)

    def onBtnPeriodClick(self):
        if self._append_period:
            return
        if '.' in self._value:
            return
        self._append_period = True



    def doOperation(self,op):
        self._last_value = self._value
        self._op=op

    def onBtnAddClick(self):
        self.doOperation("+")

    def onBtnMinusClick(self):
        self.doOperation("-")

    def onBtnMultiplyClick(self):
        self.doOperation("*")

    def onBtnDivideClick(self):
        self.doOperation("/")

    def onBtnResultClick(self):
        if self._op=="":
            return
        v1=Decimal(self._last_value)
        v2=Decimal(self._value)
        if self._op == '+':
            result = v1+v2
        if self._op == '-':
            result = v1-v2
        if self._op == '*':
            result = v1*v2
        if self._op == '/':
            result = v1/v2
        self._op = ""
        self.updateValue(str(result))


if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    main_frame = MainFrame()
    main_frame.show()
    app.exec()