from PyQt5 import QtWidgets, QtGui, QtCore
from OpenGL.GL import *

class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self._is_wire = False
        self.setFixedSize(500,500)

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)
        if self._is_wire:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glColor(0,0,0)

        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(10,90,0)
        glVertex3f(10,10,0)
        glVertex3f(35,75,0)
        glVertex3f(30,20,0)
        glVertex3f(90,90,0)
        glVertex3f(80,40,0)
        glEnd()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Space:
            self._is_wire = not self._is_wire
        self.update()

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity();
        glOrtho(0,100,0,100,-1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity();

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()