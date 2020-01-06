"""
Use vertex array to draw
"""


from PyQt5 import QtWidgets,QtGui,QtCore
from OpenGL.GL import *
import numpy as np

vertices = np.array([
    10, 90, 0,
    30, 70, 0,
    10, 10, 0,
    30, 30, 0,
    90, 10, 0,
    70, 30, 0,
    90, 90, 0,
    70, 70, 0,
],dtype = np.float32)

colors = np.array([
    0.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 0.0, 1.0,
    1.0, 1.0, 0.0,
    1.0, 0.0, 1.0,
    0.0, 1.0, 1.0,
    1.0, 0.0, 0.0
],dtype = np.float32)

stripIndices = np.array([0,1,2,3,4,5,6,7,0,1],dtype=np.uint32)
class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self._wire = False
        self.setFixedSize(500,500)

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0) # background color

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3,GL_FLOAT,0,vertices)
        glColorPointer(3,GL_FLOAT,0,colors)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)
        glColor(0,0,0)

        if self._wire:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)


        glDrawElements(GL_TRIANGLE_STRIP,10,GL_UNSIGNED_INT, stripIndices)

        glFlush()

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity();
        glOrtho(0,100,0,100,-1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity();

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Space:
            self._wire = not self._wire
            self.repaint()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()