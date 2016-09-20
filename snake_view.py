from __future__ import print_function
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPen, QColor, QBrush

from time import time

from snake_utils import *



class SnakeView(QtGui.QGraphicsView):

    abortRequested = pyqtSignal()
    upRequested    = pyqtSignal()
    dnRequested    = pyqtSignal()

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

    def _sq(self, x, y):
        rect = self.scene.addRect(x*self._size, y*self._size,
                                  self._size, self._size,
                                  pen=self._pen, brush=self._brush)
        return rect


    def __setup__(self):
        black = QColor.fromRgb(0,0,0)
        self._pen = QPen(black)
        self._brush = QBrush(black)
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

    def repaint(self, matrix, snake):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                val = matrix[i][j]
                colorize(self._grid[i][j], val)
