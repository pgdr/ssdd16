from __future__ import print_function
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPen, QColor, QBrush
from PyQt4.QtGui import QGraphicsSimpleTextItem as QText
from PyQt4.QtCore import QString

from time import time

from snake_utils import colorize



class SnakeView(QtGui.QGraphicsView):

    gameOverRequested = pyqtSignal()
    abortRequested    = pyqtSignal()
    upRequested       = pyqtSignal()
    dnRequested       = pyqtSignal()
    BLACK = QColor.fromRgb(0,0,0)
    WHITE = QColor.fromRgb(255,255,255)

    def __init__(self, width, height, size=10):
        super(SnakeView, self).__init__()
        self._keymap = {QtCore.Qt.Key_Q: self.abortRequested,
                        QtCore.Qt.Key_W: self.upRequested,
                        QtCore.Qt.Key_S: self.dnRequested}
        self._width = width   # no squares wide (i/x/m direction)
        self._height = height # no squares high (j/y/n direction)
        self._size = size     # pixels per square, e.g. 10x10
        self._grid = []
        self.__setup__()
        self._scoreItem = self.scene.addSimpleText('')
        self._prevOpt = []

    def _sq(self, x, y):
        rect = self.scene.addRect(x*self._size, y*self._size,
                                  self._size, self._size,
                                  pen=self._pen, brush=self._brush)
        return rect


    def __setup__(self):
        self._pen = QPen(SnakeView.BLACK)
        self._brush = QBrush(SnakeView.BLACK)
        self._pen.setWidth(1)
        x,y=(1+self._width) * self._size, (1+self._height) * self._size
        self.setGeometry(QtCore.QRect(0,0,x,y))
        self.scene = QtGui.QGraphicsScene(self)
        self.setScene(self.scene)

        self.installEventFilter(self)

        for i in range(self._width):
            self._grid.append([])
            for j in range(self._height):
                r = self._sq(i,j)
                self._grid[i].append(r)

    def eventFilter(self, obj, event):
        """We catch and absorb all key presses"""
        if event.type() == QEvent.KeyPress:
            k = event.key()
            if k in self._keymap:
                self._keymap[k].emit()
            return True
        else:
            return False

    def repaint(self, matrix, snake, score):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                val = matrix[i][j]
                colorize(self._grid[i][j], val)
        for (i,j) in snake:
            colorize(self._grid[i][j], 2)
        self._scoreItem.setText(str(score))

    def drawOpt(self, path):
        for x in self._prevOpt:
            self.scene.removeItem(x)
        self._prevOpt = []
        s = self._size
        p = self._pen
        p.setColor(SnakeView.WHITE)
        halfsize = s / 2.0
        for i in range(1, len(path)):
            x1,y1 = i-1, path[i-1]
            x2,y2 = i  , path[i  ]
            coords = x1*s,y1*s+halfsize,x2*s,y2*s+halfsize
            l = self.scene.addLine(*coords, pen=p)
            self._prevOpt.append(l)
