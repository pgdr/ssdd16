from __future__ import print_function
from PyQt4.QtGui import QApplication

from snake_game import SnakeGame
from snake_view import SnakeView
from snake_model_norne import SnakeModelNorne
from resslice import ResSlice

def printIntro():
    print('Welcome to QtSnake!')
    print('')
    print('Press W/Up   to move down')
    print('Press S/Down to move up')
    print('Press Q/Esc  to quit')
    print('Press Space  to toggle solution (DP)')

def main():
    height = 22
    width  = 40
    size   = 20
    timer  = 100 # ms sleep
    timelimit = 30 # game duration (seconds)

    printIntro()

    gridfile = '../norne/NORNE_ATW2013.EGRID'
    restfile = '../norne/NORNE_ATW2013.UNRST'

    app = QApplication([])
    view = SnakeView(width, height, size)
    res_slice = ResSlice(gridfile, restfile)
    model = SnakeModelNorne(res_slice, width, height)
    controller = SnakeGame(view, model, app.quit, timelimit)
    controller.run(timer)

    app.exec_()

if __name__ == '__main__':
    main()
