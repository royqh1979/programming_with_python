from PyQt5 import QtWidgets, QtGui, QtCore


class DisplayFrame(QtWidgets.QLabel):

    def __init__(self,parent):
        super().__init__(parent)
        self._memory = "0"

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        super().paintEvent(e)
        if self._memory!='0':
            p = QtGui.QPainter()
            p.begin(self)
            p.setBackground(QtCore.Qt.white)
            p.setPen(QtCore.Qt.black)
            font = QtGui.QFont(self.font())
            font.setPixelSize(20)
            p.setFont(font)
            p.drawText(4,22,"M")
            p.end()

