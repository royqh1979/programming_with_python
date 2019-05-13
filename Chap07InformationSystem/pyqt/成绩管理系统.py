from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from main import Ui_MainWindow

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui
        self.ui.setupUi(self)

        self.ui.actionNew.triggered.connect(self.do_exit)
        self.ui.actionOpen.triggered.connect(self.do_open)
        self.ui.actionAdd.triggered.connect(self.do_add)
        self.ui.actionDelete.triggered.connect(self.do_delete)

    def do_exit(self):
        self.close()

    def do_open(self):
        pass

    def do_add(self):
        self.ui.editor.setEnabled(True)

    def do_delete(self):
        pass



app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
mainWindow = MyWindow(ui)
mainWindow.show()
sys.exit(app.exec_())