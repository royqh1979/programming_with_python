from decimal import Decimal
from math import sin, cos, tan, asin, acos, atan, pi, log, factorial

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
        self._ui.btn1.clicked.connect(self.onBtn1Clicked)
        self._ui.btn2.clicked.connect(self.onBtn2Clicked)
        self._ui.btn3.clicked.connect(self.onBtn3Clicked)
        self._ui.btn4.clicked.connect(self.onBtn4Clicked)
        self._ui.btn5.clicked.connect(self.onBtn5Clicked)
        self._ui.btn6.clicked.connect(self.onBtn6Clicked)
        self._ui.btn7.clicked.connect(self.onBtn7Clicked)
        self._ui.btn8.clicked.connect(self.onBtn8Clicked)
        self._ui.btn9.clicked.connect(self.onBtn9Clicked)
        self._ui.btn0.clicked.connect(self.onBtn0Clicked)
        # 清除键
        self._ui.btnClear.clicked.connect(self.onBtnClearClicked)
        self._ui.btnCE.clicked.connect(self.onBtnCEClicked)
        self._ui.btnBackspace.clicked.connect(self.onBtnBackspaceClicked)
        # 符号键
        self._ui.btnSign.clicked.connect(self.onBtnSignClicked)
        # 小数点
        self._ui.btnPeriod.clicked.connect(self.onBtnPeriodClicked)
        # 加减乘除
        self._ui.btnAdd.clicked.connect(self.onBtnAddClicked)
        self._ui.btnMinus.clicked.connect(self.onBtnMinusClicked)
        self._ui.btnMultiply.clicked.connect(self.onBtnMultiplyClicked)
        self._ui.btnDivide.clicked.connect(self.onBtnDivideClicked)
        self._ui.btnResult.clicked.connect(self.onBtnResultClicked)
        # 函数
        self._ui.btnSin.clicked.connect(self.onBtnSinClicked)
        self._ui.btnCos.clicked.connect(self.onBtnCosClicked)
        self._ui.btnTan.clicked.connect(self.onBtnTanClicked)
        self._ui.btnCtg.clicked.connect(self.onBtnCtgClicked)
        self._ui.btnSec.clicked.connect(self.onBtnSecClicked)
        self._ui.btnArcsin.clicked.connect(self.onBtnArcsinClicked)
        self._ui.btnArccos.clicked.connect(self.onBtnArccosClicked)
        self._ui.btnArctan.clicked.connect(self.onBtnArctanClicked)
        self._ui.btnArcctg.clicked.connect(self.onBtnArcctgClicked)
        self._ui.btnLog.clicked.connect(self.onBtnLogClicked)
        self._ui.btnLn.clicked.connect(self.onBtnLnClicked)
        self._ui.btnFactorial.clicked.connect(self.onBtnFactorialClicked)
        # 内存管理
        self._ui.btnMemoryAdd.clicked.connect(self.onBtnMemoryAddClicked)
        self._ui.btnReadMemory.clicked.connect(self.onBtnReadMemoryClicked)
        self._ui.btnClearMemory.clicked.connect(self.onBtnClearMemoryClicked)

    def updateValue(self,value:str):
        if "E-" in value:
            value = "0"
        if len(value)>15:
            value = value[:15]
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

    def onBtn1Clicked(self):
        self.appendDigit("1")

    def onBtn2Clicked(self):
        self.appendDigit("2")

    def onBtn3Clicked(self):
        self.appendDigit("3")

    def onBtn4Clicked(self):
        self.appendDigit("4")

    def onBtn5Clicked(self):
        self.appendDigit("5")

    def onBtn6Clicked(self):
        self.appendDigit("6")

    def onBtn7Clicked(self):
        self.appendDigit("7")

    def onBtn8Clicked(self):
        self.appendDigit("8")

    def onBtn9Clicked(self):
        self.appendDigit("9")

    def onBtn0Clicked(self):
        self.appendDigit("0")

    def onBtnClearClicked(self):
        self._last_value="0"
        self._op = ""
        self.updateMemory("0")
        self.clearCurrentValue()

    def onBtnCEClicked(self):
        self.clearCurrentValue()


    def clearCurrentValue(self):
        self._append_period = False
        self.updateValue("0")

    def onBtnBackspaceClicked(self):
        if len(self._value)>1:
            self.updateValue(self._value[0:-1])
        else:
            self.clearCurrentValue()

    def onBtnSignClicked(self):
        if self._value == '0':
            return
        if self._value[0]=='-':
            self.updateValue(self._value[1:])
        else:
            self.updateValue("+"+self._value)

    def onBtnPeriodClicked(self):
        if self._append_period:
            return
        if '.' in self._value:
            return
        self._append_period = True



    def doOperation(self,op):
        if self._op!="":
            self.onBtnResultClicked()
        self._last_value = self._value
        self._append_period = False
        self._op=op

    def onBtnAddClicked(self):
        self.doOperation("+")

    def onBtnMinusClicked(self):
        self.doOperation("-")

    def onBtnMultiplyClicked(self):
        self.doOperation("*")

    def onBtnDivideClicked(self):
        self.doOperation("/")

    def onBtnResultClicked(self):
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
        self._append_period = False
        self._op = ""
        self.updateValue(str(result))

    def onBtnSinClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(sin(float(self._value)))
        self.updateValue(str(v))

    def onBtnCosClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(cos(float(self._value)))
        self.updateValue(str(v))

    def onBtnTanClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(tan(float(self._value)))
        self.updateValue(str(v))

    def onBtnCtgClicked(self):
        self._append_period = False
        self._op=""
        v=1/Decimal(tan(float(self._value)))
        self.updateValue(str(v))

    def onBtnSecClicked(self):
        self._append_period = False
        self._op=""
        v=1/Decimal(cos(float(self._value)))
        self.updateValue(str(v))

    def onBtnArcsinClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(asin(float(self._value)))
        self.updateValue(str(v))

    def onBtnArccosClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(acos(float(self._value)))
        self.updateValue(str(v))


    def onBtnArctanClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(atan(float(self._value)))
        self.updateValue(str(v))

    def onBtnArcctgClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(pi/2-atan(float(self._value)))
        self.updateValue(str(v))

    def onBtnLogClicked(self):
        self._append_period = False
        self._op=""
        v=Decimal(self._value)
        if v>0:
            v=v.log10()
            self.updateValue(str(v))

    def onBtnLnClicked(self):
        self._append_period = False
        self._op=""
        v=float(self._value)
        if v>0:
            v = Decimal(log(v))
            self.updateValue(str(v))

    def onBtnFactorialClicked(self):
        if "." in self._value or "-" in self._value:
            return
        self._append_period = False
        self._op=""
        v=factorial(int(self._value))
        self.updateValue(str(v))

    def updateMemory(self,value:str):
        self._ui.displayFrame._memory = value
        self._ui.displayFrame.update()

    def onBtnMAddClicked(self):
        v1=Decimal(self._ui.displayFrame._memory)
        v2=Decimal(self._value)
        result = v1+v2
        self.updateMemory(str(result))

    def onBtnMemoryAddClicked(self):
        if self._value == '0':
            return
        v1=Decimal(self._ui.displayFrame._memory)
        v2=Decimal(self._value)
        result = v1+v2
        self.updateMemory(str(result))

    def onBtnReadMemoryClicked(self):
        self._append_period = False
        self.updateValue(self._ui.displayFrame._memory)

    def onBtnClearMemoryClicked(self):
        self.updateMemory("0")

if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    main_frame = MainFrame()
    main_frame.show()
    app.exec()