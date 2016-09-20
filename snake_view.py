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

    def __init__(self):
        super(SnakeView, self).__init__()
        self._keymap = {QtCore.Qt.Key_Q: self.abortRequested,
                        QtCore.Qt.Key_W: self.upRequested,
                        QtCore.Qt.Key_S: self.dnRequested}
        self.__setup__()

    def __setup__(self):
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
            pen.setColor(heatcolor(0))
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
