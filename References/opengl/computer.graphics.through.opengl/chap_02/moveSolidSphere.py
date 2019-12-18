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
// Sumanta Guha.
"""
from typing import List

from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
import math as m

# Co-ordinates of the sphere center.
Xvalue = 0.0
Yvalue = 0.0
_depth = 0
Angle = 0.0; # Angle to rotate the sphere.

def drawTriangle(v1:List[float],v2:List[float],v3:List[float]):
    glBegin(GL_TRIANGLES)
    glNormal3f(*v1)
    glVertex3f(*v1)
    glNormal3f(*v2)
    glVertex3f(*v2)
    glNormal3f(*v3)
    glVertex3f(*v3)
    glEnd()

def normalize(v:List[float]):
    d = m.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    v[0]/=d
    v[1]/=d
    v[2]/=d


def subdivide(v1:List[float],v2:List[float],v3:List[float], depth: int):
    if depth == 0:
        drawTriangle(v1,v2,v3)
        return
    v12=[0]*3
    v23=[0]*3
    v31=[0]*3
    for i in range(3):
        v12[i]=v1[i]+v2[i]
        v23[i]=v2[i]+v3[i]
        v31[i]=v3[i]+v1[i]
    normalize(v12)
    normalize(v23)
    normalize(v31)
    subdivide(v1, v12, v31, depth - 1)
    subdivide(v2, v23, v12, depth - 1)
    subdivide(v3, v31, v23, depth - 1)
    subdivide(v12, v23, v31, depth - 1)


def mySolidSphere(depth:int):
    X = .525731112119133606
    Z = .850650808352039932
    vdata = [
        [-X, 0.0, Z], [X, 0.0, Z], [-X, 0.0, -Z], [X, 0.0, -Z],
        [0.0, Z, X], [0.0, Z, -X], [0.0, -Z, X], [0.0, -Z, -X],
        [Z, X, 0.0], [-Z, X, 0.0], [Z, -X, 0.0], [-Z, -X, 0.0]
    ]

    tindices = [
        [0, 4, 1], [0, 9, 4], [9, 5, 4], [4, 5, 8], [4, 8, 1],
        [8, 10, 1], [8, 3, 10], [5, 3, 8], [5, 2, 3], [2, 7, 3],
        [7, 10, 3], [7, 6, 10], [7, 11, 6], [11, 0, 6], [0, 1, 6],
        [6, 1, 10], [9, 0, 11], [9, 11, 2], [9, 2, 5], [7, 2, 11]]

    for i in range(20):
        subdivide(vdata[tindices[i][0]],
            vdata[tindices[i][1]],
            vdata[tindices[i][2]],depth  )


class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,500)


    def initializeGL(self) -> None:
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glEnable(GL_DEPTH_TEST)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #Set the position of the sphere.
        glTranslatef(Xvalue, Yvalue, 0)
        glRotatef(Angle, 1.0, 1.0, 1.0)
        glColor3f(0.0, 0.0, 0.0)
        mySolidSphere( _depth)
        glFlush()

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0,1.0)
        glMatrixMode(GL_MODELVIEW)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        global Xvalue,Yvalue,Angle,_depth
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
        elif event.key() == QtCore.Qt.Key_PageUp and _depth < 5 :
            _depth += 1
            self.update()
        elif event.key() == QtCore.Qt.Key_PageDown and _depth>0 :
            _depth -= 1
            self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()