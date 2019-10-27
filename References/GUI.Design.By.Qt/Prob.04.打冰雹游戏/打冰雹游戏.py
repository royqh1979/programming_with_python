from typing import List

import typing

from main_window import Ui_Form as MainWindowUi
from PyQt5 import QtCore, QtWidgets, QtGui
from datetime import datetime
import random
import math

BALL_SIZE = 35


class MyBallItem(QtWidgets.QGraphicsObject):
    clicked = QtCore.pyqtSignal()

    def __init__(self, x: float, y: float, size: float, color: QtGui.QColor):
        super().__init__()
        self.setX(x)
        self.setY(y)
        self._size = size
        self._color = color
        self._speed = 0
        self._bounding_rect = QtCore.QRectF(0, 0, size, size)

    def setColor(self, color):
        self._color = color

    def speed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def color(self):
        return self._color

    def boundingRect(self) -> QtCore.QRectF:
        return self._bounding_rect

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem,
              widget: typing.Optional[QtWidgets.QWidget]) -> None:
        painter.setPen(self._color)
        painter.setBrush(self._color)
        painter.drawEllipse(0, 0, self._size, self._size)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.clicked.emit()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._ui = MainWindowUi()
        self._ui.setupUi(self)
        self._game_timer = QtCore.QTimer()
        self._game_timer.timeout.connect(self.on_game_update)
        self._game_timer.start(100)
        self._clock_timer = QtCore.QTimer()
        self._clock_timer.timeout.connect(self.on_clock_update)
        self._clock_timer.start(1000)
        self._start_time = datetime.now()

        # 初始化难度
        self._ui.cbDifficulty.addItem("简单", 1)
        self._ui.cbDifficulty.addItem("中等", 2)
        self._ui.cbDifficulty.addItem("较难", 4)
        self._ui.cbDifficulty.addItem("高级", 8)
        self._ui.cbDifficulty.setCurrentText("简单")
        self._base_speed = 2
        self._ui.cbDifficulty.currentIndexChanged.connect(self.on_difficulty_changed)

        # 设置主显示区
        self._scene = QtWidgets.QGraphicsScene()
        self._scene.setSceneRect(0, 0, 600, 650)
        self._ui.main_view.setScene(self._scene)

        # 加入小球
        self._balls: List[MyBallItem] = []
        for i in range(10):
            x = random.randint(0, self.width() - BALL_SIZE)
            y = 0
            color = QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ball = MyBallItem(x, y, BALL_SIZE, color)
            ball.clicked.connect(self.on_ball_clicked)
            speed = self._base_speed + random.randint(0, self._base_speed)
            ball.setSpeed(speed)
            self._scene.addItem(ball)
            self._balls.append(ball)

        self._life = 5
        self._score = 0
        self._ui.txtScore.setText(f"{self._score}")
        self._ui.txtLife.setText(f"{self._life}")

        # 打开鼠标位置监控
        self.setMouseTracking(True)
        self._ui.main_view.setMouseTracking(True)
        # self.setAttribute(QtCore.Qt.WA_MouseNoMask)

    def on_difficulty_changed(self, index):
        self._base_speed = self._ui.cbDifficulty.itemData(index)
        for j in range(10):
            self.reset_ball(self._balls[j])

    def update_score(self, score):
        self._score = score
        self._ui.txtScore.setText(f"{self._score}")

    def update_life(self, life):
        self._life = life
        self._ui.txtLife.setText(f"{self._life}")

    def on_ball_clicked(self):
        ball: MyBallItem = self.sender()
        self.update_score(self._score + 1)
        self.reset_ball(ball)
        self._game_timer.stop()
        if self._score == 150 and self._ui.cbDifficulty.currentIndex() <= 2:
            self._ui.cbDifficulty.setCurrentIndex(3)
        elif self._score == 100 and self._ui.cbDifficulty.currentIndex() <= 1:
            QtWidgets.QMessageBox.information(self, "祝贺", "恭喜你过关了，增加难度，再继续！")
            self._ui.cbDifficulty.setCurrentIndex(2)
        elif self._score == 50 and self._ui.cbDifficulty.currentIndex() == 0:
            QtWidgets.QMessageBox.information(self, "加油", "太棒了，再射中50个你就过关了，增加难度，再继续！")
            self._ui.cbDifficulty.setCurrentIndex(1)
        elif self._score == 25 and self._ui.cbDifficulty.currentIndex() == 0:
            QtWidgets.QMessageBox.information(self, "鼓励", "好样的，继续努力！")
        self._game_timer.start(100)

    def reset_ball(self, ball: MyBallItem):
        ball.setX(random.randint(0, self._scene.width() - BALL_SIZE))
        ball.setY(0)
        ball.setSpeed(self._base_speed + random.randint(0, self._base_speed))
        color = QtGui.QColor(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
        ball.setColor(color)

    def on_game_update(self):
        for i in range(10):
            ball = self._balls[i]
            if ball.y() > self._scene.height():
                if self._life == 0:
                    self._game_timer.stop()
                    QtWidgets.QMessageBox.information(self, "闯关失败", "你失败了，别灰心，降低难度，请重来！")
                    index = self._ui.cbDifficulty.currentIndex()
                    if index > 0:
                        index -= 1
                    self._ui.cbDifficulty.setCurrentIndex(index)
                    self.update_score(0)
                    self.update_life(5)
                    for j in range(10):
                        self.reset_ball(self._balls[j])
                    self._start_time = datetime.now()
                    self._game_timer.start(100)
                self.update_life(self._life - 1)
                self.reset_ball(ball)
                continue
            color = ball.color()
            color = QtGui.QColor(color.red() * 0.99, color.green() * 0.99, color.blue() * 0.99)
            ball.setColor(color)
            ball.moveBy(0, ball.speed())

    def on_clock_update(self):
        now = datetime.now()
        delta = now - self._start_time
        hours, minutes, seconds = delta.seconds // 3600, delta.seconds // 60, delta.seconds % 60
        self._ui.txtTime.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self._ui.point_frame.update()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        p=QtCore.QPoint(e.x(),e.y())
        p=self.mapToGlobal(p)
        x,y=p.x(),p.y()
        p=QtCore.QPoint(self._ui.point_frame.width()/2,self._ui.point_frame.height()/2)
        p=self._ui.point_frame.mapToGlobal(p)
        x1,y1=p.x(),p.y()
        a=math.atan2(y1-y,x-x1)*180/math.pi
        self._ui.point_frame._angle=a
        self._ui.point_frame.update()




if __name__ == '__main__':
    random.seed()
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
