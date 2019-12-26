from PyQt5 import QtWidgets,QtCore
from OpenGL.GL import *
import math as m

R = 20
class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,500)

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0)
        glEnable(GL_DEPTH_TEST)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor(0,0,0)

        delta = m.pi / 20
        t = -10 * m.pi
        glBegin(GL_LINE_STRIP)
        for i in range(401):
            # glVertex3f(R*m.cos(t),R*m.sin(t),t-60)
            glVertex3f(R*m.cos(t),t,R*m.sin(t)-60)
            t += delta
        glEnd()
        glFlush()

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-50,50,-50,50,0,100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()