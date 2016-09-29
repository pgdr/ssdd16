from PyQt4.QtCore import QTimer

from time import time
from math import sqrt

from ga_dpapi import dynamicProgrammingTable as DPT
from ga_dpapi import dynamicProgramming as DP

class GeneticSnakeGame():

    def __init__(self, view, model, exit_function, matrix,
                 iterations = 100, poolsize = 20, optlimit=1.0, numlines=10):
        self._view = view
        self._model = model
        self._exit = exit_function
        self._timer = QTimer()
        self._timer.timeout.connect(self.update)
        self._user_request = None # None, 'up' or 'dn'
        self._matrix = matrix
        self._dp = None
        self._dpt = DPT(self._matrix)
        self._opt = DP(self._matrix)
        self._drawn = False

    def __iterate(self):
        pass
        
    def update(self):
        if not self._drawn:
            self._model.updateColors(self._matrix)
            self._view.repaint(self._model.matrix(),[])
            self._drawn = True
            self._view.drawDp(self._opt)
            self._view.drawDpt(self._dpt)

    def run(self, timer=100):
        self._timer.start(timer)
        self._interval = self._timer.interval()

        self._view.abortRequested.connect(self._exit)
        self._view.gameOverRequested.connect(self._exit)
        self._view.show()
