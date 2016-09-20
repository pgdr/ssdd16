from __future__ import print_function
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPen, QColor, QBrush

from time import sleep, time
from math import sqrt
from random import random, randint
import colorsys

def ri(x):
    return randint(0,x-1)

def soil(x):
    val = random() + (1-abs(1.5 - x))
    return max(0, min(val, 1))

def pseudocolor(val, minval=0, maxval=1):
    h = (float(val-minval) / (maxval-minval)) * 120
    r, g, b = colorsys.hsv_to_rgb(h/360, 1., 1.)
    return QColor.fromRgb(int(r*255), int(g*255), int(b*255))

def colorize(obj, val):
    """Takes and q object and colors it with val"""
    pen,brush = obj.pen(), obj.brush()
    c = pseudocolor(val)
    pen.setColor(c)
    brush.setColor(c)
    obj.setPen(pen)
    obj.setBrush(brush)


class SnakeModel():
    def __init__(self, x=20,y=10):
        self._x = x
        self._y = y
        self._grid = []
        for i in range(x):
            c = []
            for j in range(y):
                c.append(ri(10))
            self._grid.append(c)

    def nextColumn():
        c = []
        for i in range(self._y):
            c.append(abs(soil(i/10.0))/5)
        return self._grid.append(c)


    def updateColors(grid):
        height,width=self._y,self._x
        for i in range(0,width-1):
            for j in range(height):
                grid[i][j] = grid[i+1][j]

        col = column(height)
        for i in range(height):
            colorize(grid[width-1][i], col[i])


class SnakeGame():
    def __init__(self, view, model, app):
        self._view = view
        self._model = model
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(view.repaint)
        self._timer.start(10)
        view.abortRequested.connect(app.quit)
        view.show()


class SnakeView(QtGui.QGraphicsView):

    abortRequested = pyqtSignal()
    upRequested    = pyqtSignal()
    dnRequested    = pyqtSignal()

    def __init__(self):
        super(SnakeView, self).__init__()
        self._keymap = {QtCore.Qt.Key_Q: self.abortRequested,
                        QtCore.Qt.Key_W: self.upRequested,
                        QtCore.Qt.Key_S: self.dnRequested}

        rg = QColor.fromRgb(0,0,0)
        pen = QPen(rg)
        brush = QBrush(rg)
        pen.setWidth(1)
        self.setGeometry(QtCore.QRect(0,0,800,400))
        self.scene = QtGui.QGraphicsScene(self)
        self.setScene(self.scene)

        self.installEventFilter(self)

        self._rects = []
        for i in range(20):
            pen.setColor(pseudocolor(0))
            rect = self.scene.addRect(30*i,10*i,10,10,pen=pen,brush=brush)
            self._rects.append(rect)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            k = event.key()
            if k in self._keymap:
                self._keymap[k].emit()
            return True
        else:
            return False

    def repaint(self):
        rect = self._rects[ri(20)]
        colorize(rect, soil((int(time()) % 10) / 10.0))



def main():
    #global height, width, size, TIMELIMIT
    app = QtGui.QApplication([])
    view = SnakeView()
    model = SnakeModel()
    controller = SnakeGame(view, model, app)

    app.exec_()

if __name__ == '__main__':
    main()

