"""
// hemisphere.py
//
// This program approximates a hemisphere with an array of latitudinal triangle strips.
//
// Interaction:
// Press P/p to increase/decrease the number of longitudinal slices.
// Press Q/q to increase/decrease the number of latitudinal slices.
// Press x, X, y, Y, z, Z to turn the hemisphere.
//
"""
import math as m
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *

R = 5.0  # Radius of hemisphere
p = 6    # Number of longitudinal slices.
q = 4    # Number of latitudinal slices.
# Angles to rotate hemisphere.
Xangle = 0.0
Yangle = 0.0
Zangle = 0.0

class MyWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,500)

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0)
        glEnableClientState(GL_VERTEX_ARRAY)
        self.calculate()

    def update(self) -> None:
        self.calculate()
        super().update()

    def calculate(self) -> None:
        self._vertices= np.empty((q,6*(p+1)),dtype=np.float)
        delta1=1/q * m.pi / 2
        delta2=2/p*m.pi
        for j in range(q):
            for i in range(p + 1):
                self._vertices[j][i*6]= R * m.cos((j + 1) * delta1) * m.cos(i * delta2)
                self._vertices[j][i*6+1]= R * m.sin((j + 1) * delta1)
                self._vertices[j][i*6+2]= R * m.cos((j + 1) * delta1) * m.sin(i * delta2)
                self._vertices[j][i*6+3]= R * m.cos(j * delta1) * m.cos(i * delta2)
                self._vertices[j][i*6+4] = R * m.sin(j * delta1)
                self._vertices[j][i*6+5] = R * m.cos(j * delta1) * m.sin(i * delta2)

    def paintGL(self) -> None:
        glClear (GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Command to push the hemisphere, which is drawn centered at the origin,
        # into the viewing frustum.
        glTranslatef(0.0, 0.0, -10.0)

        # Commands to turn the hemisphere.
        glRotatef(Zangle, 0.0, 0.0, 1.0)
        glRotatef(Yangle, 0.0, 1.0, 0.0)
        glRotatef(Xangle, 1.0, 0.0, 0.0)
   
        # Hemisphere properties.
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(0.0, 0.0, 0.0)

        # Array of latitudinal triangle strips, each parallel to the equator, stacked one
        # above the other from the equator to the north pole.

        # for j in range(q):
        #     # One latitudinal triangle strip.
        #     glVertexPointer(3,GL_FLOAT,0,self._vertices[j])
        #     # glDrawElements(GL_TRIANGLE_STRIP,2*(p+1),GL_UNSIGNED_INT,list(range(2*(p+1))))
        #     glDrawArrays(GL_TRIANGLE_STRIP,0,2*(p+1))
        glVertexPointer(3, GL_FLOAT, 0, self._vertices)
        glMultiDrawArrays(GL_TRIANGLE_STRIP,np.arange(0,2*(p+1)*q,2*(p+1)),np.repeat(2*(p+1),q),q)

        glFlush()

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        global p,q,Xangle,Yangle,Zangle
        key = event.key()
        mod = event.modifiers()
        if key == Qt.Key_P and mod != Qt.ShiftModifier and p<50:
            p+=1
            self.update()
        elif key == Qt.Key_P and mod == Qt.ShiftModifier and p>6:
            p-=1
            self.update()
        elif key == Qt.Key_Q and mod != Qt.ShiftModifier and q<50:
            q+=1
            self.update()
        elif key == Qt.Key_Q and mod == Qt.ShiftModifier and q>4:
            q-=1
            self.update()
        elif key == Qt.Key_X:
            if mod != Qt.ShiftModifier:
                Xangle += 5.0
            else:
                Xangle -= 5.0
            Xangle %= 360
            self.update()
        elif key == Qt.Key_Y:
            if mod != Qt.ShiftModifier:
                Yangle += 5.0
            else:
                Yangle -= 5.0
            Yangle %= 360
            self.update()
        elif key == Qt.Key_Z:
            if mod != Qt.ShiftModifier:
                Zangle += 5.0
            else:
                Zangle -= 5.0
            Zangle %= 360
            self.update()

if __name__ == '__main__':
    app = QApplication([])
    win = MyWidget()
    win.show()
    app.exec()
