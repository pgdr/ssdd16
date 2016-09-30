from PyQt4.QtCore import QTimer

from time import time
from math import sqrt

from sa_snake_individual import SimulatedSnakeIndividual
from sa_snake_sa import SimulatedSnakeSimulatedAnnealing

from sa_dpapi import dynamicProgramming as DP

class SimulatedSnakeGame():

    def __init__(self, view, model, exit_function, matrix,
                 iterations = 100, temperature = 20, optlimit=1.0):
        self._view = view
        self._model = model
        self._exit = exit_function
        self._timer = QTimer()
        self._timer.timeout.connect(self.update)
        self._user_request = None # None, 'up' or 'dn'
        self._matrix = matrix
        self._dp = None
        self._iterations = iterations
        self._temperature = temperature
        self._sa = SimulatedSnakeSimulatedAnnealing(self._matrix, SimulatedSnakeIndividual.randomIndividual, temperature)
        self._best = self._sa.best()
        self._best_repeated = 0
        self._optlimit = optlimit
        self._optsnake = self.__dpsnake()
        self._opt = self._optsnake.fitness()
        self._drawn = False

    def __dpsnake(self):
        optsnake = DP(self._matrix)
        return SimulatedSnakeIndividual(self._matrix, individual=optsnake)


    def __iterate(self):
        sa = self._sa
        sa.iteration(its=self._iterations)
        b = sa.best()
        if b > self._best:
            print('Best individual: (%.2f) %s' % (b.fitness(),b))
            self._best_repeated = 0
            self._best = b
            if b.fitness() >= self._opt * self._optlimit:
                print('Reached %d%% of opt.  Exit.' % int(100.0*self._optlimit))
                self._exit()

    def dp(self):
        if self._dp:
            self._dp = None
            return
        self._dp = self._optsnake
        print('OPT (DP): %.2f' % self._dp.fitness())

    def update(self):
        if not self._drawn:
            self._model.updateColors(self._matrix)
            self._view.repaint(self._model.matrix(),[])
            self._drawn = True
        else:
            self.__iterate()
        self._view.drawOpt(self._sa.best())
        self._view.drawDp(self._dp)
        self._view.drawTopTen(self._sa.prev())

    def run(self, timer=100):
        self._timer.start(timer)
        self._interval = self._timer.interval()

        self._view.abortRequested.connect(self._exit)
        self._view.gameOverRequested.connect(self._exit)
        self._view.dpRequested.connect(self.dp)
        self._view.show()
