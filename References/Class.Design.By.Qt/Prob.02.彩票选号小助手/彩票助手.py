from front_dlg import Ui_Dialog as FrontDialogUi
from PyQt5 import QtWidgets,QtCore,QtGui
from sports_lottery_dialog import SportsLotteryDialog
from welfare_lottery_dialog import WelfareLotteryDialog

class MainDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = FrontDialogUi()
        self.ui.setupUi(self)
        self.ui.btnSportLottery.clicked.connect(self.show_sports_lottery_dialog)
        self.ui.btnWelfareLottery.clicked.connect(self.show_welfare_lottery_dialog)

    def show_sports_lottery_dialog(self):
        self.hide()
        sports_dlg = SportsLotteryDialog()
        sports_dlg.show()
        sports_dlg.exec()
        self.show()

    def show_welfare_lottery_dialog(self):
        self.hide()
        dialog = WelfareLotteryDialog()
        dialog.show()
        dialog.exec()
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        app.quit()


if __name__=='__main__':
    app=QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    dialog = MainDialog()
    dialog.show()
    app.exec()
