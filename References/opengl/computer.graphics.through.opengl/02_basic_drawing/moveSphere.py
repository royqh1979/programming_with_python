"""
// moveSphere.py
//
// This program allows the user to move a sphere to demonstrate
// distortion at the edges of the viewing frustum.
//
// Interaction:
// Press the arrow keys to move the sphere.
// Press the space bar to rotate the sphere..
// Press r to reset.
//
"""

from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
import math as m

# Co-ordinates of the sphere center.
Xvalue = 0.0
Yvalue = 0.0

Angle = 0.0; # Angle to rotate the sphere.

def myWireSphere(r:float, nParal:int, nMerid:int):
    j=0
    while j<m.pi:
        glBegin(GL_LINE_LOOP)
        y=r*m.cos(j)
        i=0
        while i < 2*m.pi:
            x=r*m.cos(i)*m.sin(j)
            z=r*m.sin(i)*m.sin(j)
            glVertex3f(x,y,z)
            i += m.pi / 60
        glEnd();
        j += m.pi / (nParal + 1)

    j=0
    while j<m.pi:
        glBegin(GL_LINE_LOOP)
        i=0
        while i < 2*m.pi:
            x=r*m.sin(i)*m.cos(j)
            y=r*m.cos(i)
            z=r*m.sin(j)*m.sin(i)
            glVertex3f(x,y,z)
            i += m.pi / 60
        glEnd();
        j += m.pi / nMerid

class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,500)


    def initializeGL(self) -> None:
        glClearColor(1.0, 1.0, 1.0, 0.0)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)

        glLoadIdentity()

        #Set the position of the sphere.
        glTranslatef(Xvalue, Yvalue, -5.0)
        glRotatef(Angle, 1.0, 1.0, 1.0)
        glColor3f(0.0, 0.0, 0.0)
        myWireSphere(0.5, 16, 10)
        glFlush()

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
        glMatrixMode(GL_MODELVIEW)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        global Xvalue,Yvalue,Angle
        if event.key() == QtCore.Qt.Key_R:
            Xvalue = Yvalue = Angle = 0.0
            self.update()
        elif event.key() == QtCore.Qt.Key_Space:
            Angle += 10.0
            self.update()
        elif event.key() == QtCore.Qt.Key_Up:
            Yvalue += 0.1
            self.update()
        elif event.key() == QtCore.Qt.Key_Down:
            Yvalue -= 0.1
            self.update()
        elif event.key() == QtCore.Qt.Key_Left:
            Xvalue -= 0.1
            self.update()
        elif event.key() == QtCore.Qt.Key_Right:
            Xvalue += 0.1
            self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()