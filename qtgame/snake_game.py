from PyQt4 import QtCore

from snake_model import SnakeModel
from snake_view import SnakeView

from time import time
from math import sqrt

from dpapi import dynamicProgramming as DP

class SnakeGame():
    UP = 1
    DN = 2
    def __init__(self, view, model, exit_function, timelimit=30):
        self._view = view
        self._model = model
        self._exit = exit_function
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update)
        self._user_request = None # None, 'up' or 'dn'

        self._score = 0
        self._timelimit = timelimit
        self._start = time()

    def up(self):
        self._user_request = SnakeGame.UP

    def dn(self):
        self._user_request = SnakeGame.DN

    def currentTimeScore(self):
        ctime = time()
        playtime = ctime - self._start
        remaining = self._timelimit - playtime
        return remaining

    def update(self):
        remaining = self.currentTimeScore()

        # update score
        val = self._model.snakeHeadValue()
        self._score += sqrt(val / 120.0)
        l = len(self._model.snake())
        if self._score >= l:
            self._model.snakeGrow()

        # time out
        if remaining < 0:
            print('Loser')
            self._view.gameOverRequested.emit()

        # snake reached end of board (left-most side)
        if l >= self._model.width() / 2:
            print('Your score: %.2f' % remaining)
            self._view.gameOverRequested.emit()

        # go up or down according to user request
        req = self._user_request
        self._user_request = None
        if req == SnakeGame.UP:
            self._model.snakeUp()
        elif req == SnakeGame.DN:
            self._model.snakeDn()

        self._model.updateColors()
        self._view.repaint(self._model.matrix(), self._model.snake(), '%.2f'%remaining)

        opt = DP(self._model.matrix())
        self._view.drawOpt(opt)

    def run(self, timer=100):
        self._timer.start(timer)
        self._view.abortRequested.connect(self._exit)
        self._view.gameOverRequested.connect(self._exit)
        self._view.upRequested.connect(self.up)
        self._view.dnRequested.connect(self.dn)
        self._view.show()
