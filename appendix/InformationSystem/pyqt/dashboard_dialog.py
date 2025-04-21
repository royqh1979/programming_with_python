from matplotlib.axes import Axes

from dashboard import Ui_Dialog
from PyQt5 import QtWidgets
from enum import Enum
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
import numpy as np


font_name = "STKaiti"
mpl.rcParams['font.family'] = font_name
mpl.rcParams['axes.unicode_minus'] = False  # in case minus sign is shown as box

class ChartType(Enum):
    PieChart = 0
    Histogram = 1



class DashboardDialog(QtWidgets.QDialog):
    def __init__(self,parent,students,type):
        super().__init__(parent)
        self.students = students
        ui = Ui_Dialog()
        ui.setupUi(self)
        self.ui = ui
        self.ui.btnOk.clicked.connect(self.close)
        self._init_chart_types(type)
        self._init_figure()
        self.display()

    def _init_chart_types(self,default_type):
        cb_type = self.ui.cbChartType
        for type in ChartType:
            cb_type.addItem(type.name)
        cb_type.setCurrentText(default_type.name)
        cb_type.setEditable(False)
        cb_type.currentTextChanged.connect(self.display)

    def _init_figure(self):
        figure = Figure()
        canvas = FigureCanvas(figure)
        layout = QtWidgets.QVBoxLayout(self.ui.chartWidget)
        layout.addWidget(canvas)
        self.ui.chartWidget.setLayout(layout)
        self.figure = figure

    def display(self):
        text = self.ui.cbChartType.currentText()
        if text == ChartType.PieChart.name:
            self.draw_pie_chart()
            return
        if text == ChartType.Histogram.name:
            self.draw_histogram()
            return


    def draw_pie_chart(self):
        counts = self.calc_counts()
        self.figure.clf()
        axes = self.figure.subplots()
        axes.pie(counts, labels=[f"{x * 10}-{(x + 1) * 10 - 1}" for x in range(10)])
        axes.set_title("各分数段人数")
        self.figure.canvas.draw()

    def draw_histogram(self):
        print("2")
        counts = self.calc_counts()
        self.figure.clf()
        axes = self.figure.subplots()
        axes.bar([f"{x * 10}-{(x + 1) * 10 - 1}" for x in range(10)], counts)
        axes.set_title("各分数段人数")
        axes.set_xlabel("分数段")
        axes.set_ylabel("人数")
        self.figure.canvas.draw()


    def calc_counts(self):
        counts = [0] * 10
        for id in self.students:
            s = self.students[id]
            score = s.score
            if round(score) >= 100:
                counts[9] += 1
            else:
                counts[round(score) // 10] += 1
        return counts