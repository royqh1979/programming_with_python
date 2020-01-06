from PyQt5 import QtWidgets,QtGui,QtCore
from OpenGL.GL import *

class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self._wire = False
        self.setFixedSize(500,500)

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0) # background color

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)
        glColor(0,0,0)

        if self._wire:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)


        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(10,90,0)
        glVertex3f(30,70,0)
        glVertex3f(10,10,0)
        glVertex3f(30,30,0)
        glVertex3f(90,10,0)
        glVertex3f(70,30,0)
        glVertex3f(90,90,0)
        glVertex3f(70,70,0)
        glVertex3f(10,90,0)
        glVertex3f(30,70,0)
        glEnd()

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
            self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()