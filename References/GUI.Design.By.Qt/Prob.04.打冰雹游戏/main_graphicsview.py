from PyQt5 import QtWidgets,QtGui

class MainGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self,parent):
        super().__init__(parent)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        event.ignore()