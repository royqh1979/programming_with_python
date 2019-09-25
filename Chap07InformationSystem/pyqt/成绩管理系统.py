import csv
from typing import List, Dict

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from main import Ui_MainWindow
from student import Student
from dashboard_dialog import DashboardDialog, ChartType


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui
        self.ui.setupUi(self)
        self.ui.actionExit.triggered.connect(self.do_exit)
        self.ui.actionNew.triggered.connect(self.do_new)
        self.ui.actionOpen.triggered.connect(self.do_open)
        self.ui.actionSave.triggered.connect(self.do_save)
        self.ui.actionSave_As.triggered.connect(self.do_save_as)
        self.ui.actionAdd.triggered.connect(self.do_add)
        self.ui.actionDelete.triggered.connect(self.do_delete)
        self.ui.actionPiechart.triggered.connect(self.show_piechart)
        self.ui.actionHistogram.triggered.connect(self.show_histogram)
        self.ui.btnOK.clicked.connect(self.modify_ok)
        self.ui.btnCancel.clicked.connect(self.modify_cancle)
        self.ui.tblStudents.cellDoubleClicked.connect(self.do_modify)
        self.init_status_bar()

        self.students: Dict[str, Student] = {}
        self.init_table()
        self.is_adding = False
        self.data_file = None

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        """
        覆写QMainWindow's的CloseEvent()方法

        当主窗口右上角的X（关闭）按钮被点下时，该方法会被调用

        :param e:
        :return:
        """
        self.do_exit()

    def do_exit(self):
        """
        退出程序
        """
        self.close()

    def do_new(self):
        """
        新建空白表格
        """
        self.data_file = None
        self.students.clear()
        self.update_table()

    def do_open(self):
        """
        打开数据文件
        """
        result = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "打开文件",
                                                         "",
                                                         "CSV文件 (*.csv);;所有文件(*.*)")
        filename = result[0]
        if filename == '':
            return
        students = {}
        try:
            with open(filename, mode="r", encoding="GBK") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    id = row[0]
                    name = row[1]
                    class_name = row[2]
                    score = float(row[3])
                    if id in self.students.keys():
                        raise ValueError(f"载入失败：学号{id}已存在！")
                    student = Student(id, name, class_name, score)
                    students[id] = student
        except Exception as e:
            QtWidgets.QMessageBox.warning("打开数据文件失败！",
                                          str(e),QtWidgets.QMessageBox.Close)
            return

        self.data_file = filename
        self.students = students
        self.update_table()
        self.ui.statusbar.showMessage('数据载入完成',5000)

    def do_save(self):
        """
        保存到数据文件
        """
        if self.data_file is None:
            self.do_save_as()
        else:
            self.save(self.data_file)

    def do_save_as(self):
        """
        另存为数据文件
        """
        result = QtWidgets.QFileDialog.getSaveFileName(self,
                                                       "保存文件",
                                                       "",
                                                       "CSV文件 (*.csv);;所有文件(*.*)")
        filename = result[0]
        if filename == '':
            return
        self.save(filename)
        self.data_file = filename

    def save(self,filename):
        """
        保存到指定文件

        :param filename: 要保存的文件路径
        """
        print("lala")
        try:
            with open(filename,mode="w",encoding="GBK") as file:
                file.write("学号,姓名,班级,成绩\n")
                for id in self.students:
                    s = self.students[id]
                    file.write(f"{s.id},{s.name},{s.class_name},{s.score}\n")
            self.ui.statusbar.showMessage('数据保存完成', 5000)
            return True
        except Exception as e:
            QtWidgets.QMessageBox.warning("保存数据文件失败！",
                                          str(e),QtWidgets.QMessageBox.Close)
            return False

    def do_add(self):
        """
        添加学生记录
        """
        self.ui.tblStudents.setEnabled(False)
        self.ui.editor.setEnabled(True)
        self.is_adding = True

    def do_modify(self, row, column):
        """
        修改学生记录（双击单元格时触发）

        :param row: 行号
        :param column: 列号
        """
        self.ui.tblStudents.setEnabled(False)
        self.ui.editor.setEnabled(True)
        self.is_adding = False
        id = self.ui.tblStudents.item(row,0).text()
        s = self.students[id]
        self.ui.txtId.setText(s.id)
        self.ui.txtId.setEnabled(False)
        self.ui.txtName.setText(s.name)
        self.ui.txtClass.setText(s.class_name)
        self.ui.txtScore.setText(str(s.score))

    def modify_ok(self):
        """
        完成添加或者修改
        """
        sorting_enabled = self.ui.tblStudents.isSortingEnabled()  # 保存原有排序设置
        self.ui.tblStudents.setSortingEnabled(False)
        id = self.ui.txtId.text()
        name = self.ui.txtName.text()
        class_name = self.ui.txtClass.text()
        score = float(self.ui.txtScore.text())
        s = Student(id, name, class_name, score)
        if self.is_adding:
            if id in self.students:
                QtWidgets.QMessageBox.warning("添加失败"
                                              "学号已存在",
                                              QtWidgets.QMessageBox.Close)
                return
            self.is_adding = False
            self.students[id] = s
            n = len(self.students)
            self.ui.tblStudents.setRowCount(n)
            self.set_row(n - 1, s)
            self.ui.actionDelete.setEnabled(True)
        else:
            i = self.ui.tblStudents.currentIndex().row()
            self.students[id] = s
            sorting_enabled = self.ui.tblStudents.isSortingEnabled()  # 保存原有排序设置
            self.set_row(i,s)

        self.clear_editor()
        self.ui.tblStudents.setSortingEnabled(sorting_enabled)
        self.update_student_info()

    def modify_cancle(self):
        """
        取消添加或者修改

        """
        self.clear_editor()

    def clear_editor(self):
        self.ui.txtId.setEnabled(True)
        self.ui.txtId.setText('')
        self.ui.txtName.setText('')
        self.ui.txtClass.setText('')
        self.ui.txtScore.setText('')
        self.ui.tblStudents.setEnabled(True)
        self.ui.editor.setEnabled(False)

    def do_delete(self):
        """
        删除选中的学生记录
        """
        i = self.ui.tblStudents.currentIndex().row()
        id = self.ui.tblStudents.item(i,0).text()
        del self.students[id]
        self.ui.tblStudents.removeRow(i)
        if self.ui.tblStudents.rowCount() <= 0:
            self.ui.actionDelete.setEnabled(False)
        self.update_student_info()

    def init_table(self):
        """
        初始化表格设置
        """
        self.ui.tblStudents.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tblStudents.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.tblStudents.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.tblStudents.setColumnCount(4)
        self.ui.tblStudents.setHorizontalHeaderLabels(['学号', '姓名', '班级', '成绩'])
        self.ui.tblStudents.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.ui.tblStudents.setSortingEnabled(True)
        self.update_table()

    def update_table(self):
        """
        更新表格内容
        """
        if len(self.students) == 0:
            self.ui.tblStudents.setRowCount(0)
            self.ui.actionDelete.setEnabled(False)
            return
        else:
            self.ui.actionDelete.setEnabled(True)
        tbl_students = self.ui.tblStudents
        sorting_enabled = tbl_students.isSortingEnabled()  # 保存原有排序设置
        tbl_students.setSortingEnabled(False)
        tbl_students.setRowCount(len(self.students))
        i=0
        for id in self.students:
            s = self.students[id]
            self.set_row(i, s)
            i+=1
        tbl_students.setSortingEnabled(sorting_enabled)
        self.update_student_info()

    def init_status_bar(self):
        self.ui.count_info = QtWidgets.QLabel('')
        self.ui.statusbar.addPermanentWidget(self.ui.count_info)

    def update_student_info(self):
        msg = f"共有{len(self.students)}个学生"
        self.ui.count_info.setText(msg)

    def set_row(self, i , s):
        """
        设置表格的一行内容

        :param i: 哪一行
        :param s: 用哪个学生的信息填充
        :return:
        """
        tbl_students = self.ui.tblStudents
        item = QtWidgets.QTableWidgetItem(s.id)
        tbl_students.setItem(i, 0, item)
        item = QtWidgets.QTableWidgetItem(s.name)
        tbl_students.setItem(i, 1, item)
        item = QtWidgets.QTableWidgetItem(s.class_name)
        tbl_students.setItem(i, 2, item)
        item = QtWidgets.QTableWidgetItem(str(s.score))
        tbl_students.setItem(i, 3, item)

    def show_piechart(self):
        dashboard = DashboardDialog(self,self.students,ChartType.PieChart)
        dashboard.exec()

    def show_histogram(self):
        dashboard = DashboardDialog(self,self.students,ChartType.Histogram)
        dashboard.exec()


app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
mainWindow = MyWindow(ui)
mainWindow.show()
sys.exit(app.exec_())
