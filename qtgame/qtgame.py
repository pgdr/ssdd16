from __future__ import print_function
from PyQt4.QtGui import QApplication

from snake_game import SnakeGame
from snake_view import SnakeView
from snake_model import SnakeModel
from os.path import isfile

try:
    from snake_model_norne import SnakeModelNorne
    from resslice import ResSlice
except:
    print('No ERT support')

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
    timer  = 60 # ms sleep
    timelimit = 100 # game duration (seconds)

    gridfile = 'norne.EGRID'
    restfile = 'norne.UNRST'
    if not isfile(gridfile) or not isfile(restfile):
        print('Needs norne.EGRID and norne.UNRST to play norne.')

    printIntro()

    app = QApplication([])
    view = SnakeView(width, height, size)
    model = None
    try:
        res_slice = ResSlice(gridfile, restfile)
        model = SnakeModelNorne(res_slice, width, height)
    except:
        model = SnakeModel(width, height)
    controller = SnakeGame(view, model, app.quit, timelimit)
    controller.run(timer)

    app.exec_()

if __name__ == '__main__':
    main()
