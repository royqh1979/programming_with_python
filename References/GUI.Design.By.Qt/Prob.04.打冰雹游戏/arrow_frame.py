from PyQt5 import QtWidgets, QtGui, QtCore


class ArrowFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._angle = 0

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        height = self.height() * 0.45
        x1, y1 = 0, -height
        x2, y2 = height * 0.3, -height * .065
        x3, y3 = -x2, y2
        x4, y4 = height * 0.1, y2
        x5, y5 = -x4, y4
        x6, y6 = 0, height
        p = QtGui.QPainter()
        p.begin(self)
        p.setPen(QtGui.QColor(QtCore.Qt.black))
        p.translate(self.width() / 2, self.height() / 2)
        p.rotate(90-self._angle)
        p.drawLine(x1, y1, x2, y2)
        p.drawLine(x1, y1, x3, y3)
        p.drawLine(x2, y2, x4, y4)
        p.drawLine(x3, y3, x5, y5)
        p.drawLine(x4, y4, x6, y6)
        p.drawLine(x5, y5, x6, y6)
        p.end()
