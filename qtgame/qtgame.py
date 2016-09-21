from __future__ import print_function
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPen, QColor, QBrush

from random import random, randint
import colorsys

from snake_game import SnakeGame
from snake_view import SnakeView
from snake_model import SnakeModel

def main():
    height = 20
    width  = 50
    size   = 20
    timer  = 100 # ms sleep

    app = QtGui.QApplication([])
    view = SnakeView(width, height, size)
    model = SnakeModel(width,height)
    controller = SnakeGame(view, model, app)
    controller.run(timer)

    app.exec_()

if __name__ == '__main__':
    main()

