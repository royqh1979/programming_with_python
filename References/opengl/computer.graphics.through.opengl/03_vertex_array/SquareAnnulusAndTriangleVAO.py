"""
Use vertex buffer object (VBO) to draw
"""


from PyQt5 import QtWidgets,QtGui,QtCore
from OpenGL.GL import *
from OpenGL.arrays import vbo
from ctypes import c_void_p
import numpy as np

vertices1 = np.array([
    10, 90, 0,
    30, 70, 0,
    10, 10, 0,
    30, 30, 0,
    90, 10, 0,
    70, 30, 0,
    90, 90, 0,
    70, 70, 0,
],dtype = np.float32)

colors1 = np.array([
    0.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 0.0, 1.0,
    1.0, 1.0, 0.0,
    1.0, 0.0, 1.0,
    0.0, 1.0, 1.0,
    1.0, 0.0, 0.0
],dtype = np.float32)

# Vertex position vectors for the triangle.
vertices2 = np.array(
[
	40.0, 40.0, 0.0,
    60.0, 40.0, 0.0,
    60.0, 60.0, 0.0
],dtype=np.float32)

# Vertex color vectors for the triangle.
colors2 = np.array(
[
	0.0, 1.0, 1.0,
    1.0, 0.0, 0.0,
    0.0, 1.0, 0.0
], dtype=np.float32)

stripIndices = np.array([0,1,2,3,4,5,6,7,0,1],dtype=np.uint32)

class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self._wire = False
        self.setFixedSize(500,500)

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0) # background color

        self.vaos = glGenVertexArrays(2)

        # begin binding vao 1
        glBindVertexArray(self.vaos[0])
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        new_array = np.concatenate((vertices1, colors1))
        self.vbo1 = vbo.VBO(new_array)
        self.index_vbo1 = vbo.VBO(stripIndices, target=GL_ELEMENT_ARRAY_BUFFER)
        self.vbo1.bind()
        glVertexPointer(3,GL_FLOAT,0,c_void_p(0)) # replace c_void_p(0) with None also do the work.
        glColorPointer(3, GL_FLOAT, 0, c_void_p(vertices1.size * vertices1.itemsize))
        self.index_vbo1.bind()
        # end binding vao 1
        glBindVertexArray(0)
        self.index_vbo1.unbind()
        self.vbo1.unbind()

        # begin binding vao 2
        glBindVertexArray(self.vaos[1])
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        new_array = np.concatenate((vertices2, colors2))
        self.vbo2 = vbo.VBO(new_array)
        self.vbo2.bind()
        glVertexPointer(3,GL_FLOAT,0,c_void_p(0)) # replace c_void_p(0) with None also do the work.
        glColorPointer(3, GL_FLOAT, 0, c_void_p(vertices2.size * vertices2.itemsize))
        # end binding vao 2
        glBindVertexArray(0)

        self.vbo2.unbind()

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)
        glColor(0,0,0)

        if self._wire:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)


        glBindVertexArray(self.vaos[0])
        glDrawElements(GL_TRIANGLE_STRIP,10,GL_UNSIGNED_INT, None)

        glBindVertexArray(self.vaos[1])
        glDrawArrays(GL_TRIANGLES, 0, 3)

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