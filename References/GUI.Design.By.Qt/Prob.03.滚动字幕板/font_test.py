#列出系统中的所有字体名称
from PyQt5 import QtCore,QtGui,QtWidgets

app=QtGui.QGuiApplication([])
database = QtGui.QFontDatabase()

for family in database.families():
    print(family)

