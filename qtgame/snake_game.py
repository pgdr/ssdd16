from PyQt4 import QtCore

from snake_model import SnakeModel
from snake_view import SnakeView

class SnakeGame():
    UP = 1
    DN = 2
    def __init__(self, view, model, app):
        self._view = view
        self._model = model
        self._app = app
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update)
        self._user_request = None # None, 'up' or 'dn'

    def up(self):
        self._user_request = SnakeGame.UP

    def dn(self):
        self._user_request = SnakeGame.DN

    def update(self):
        req = self._user_request
        self._user_request = None
        if req == SnakeGame.UP:
            self._model.snakeUp()
        elif req == SnakeGame.DN:
            self._model.snakeDn()

        self._view.repaint(self._model.matrix(), self._model.snake())

    def run(self):
        self._timer.start(10)
        self._view.abortRequested.connect(self._app.quit)
        self._view.upRequested.connect(self.up)
        self._view.dnRequested.connect(self.dn)
        self._view.show()
