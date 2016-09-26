from PyQt4.QtCore import QTimer

from time import time
from math import sqrt

from ga_snake_individual import GeneticSnakeIndividual
from ga_snake_ga import GeneticSnakeGeneticAlgorithm

class GeneticSnakeGame():

    def __init__(self, view, model, exit_function, matrix, iterations = 100, size = 20):
        self._view = view
        self._model = model
        self._exit = exit_function
        self._timer = QTimer()
        self._timer.timeout.connect(self.update)
        self._user_request = None # None, 'up' or 'dn'
        self._matrix = matrix
        self._dp = None
        self._iterations = iterations
        self.__setup(size)
        self._best = self._ga.best()

    def __setup(self, size = 15):
        pool = set()
        for i in range(size):
            pool.add(GeneticSnakeIndividual.randomIndividual(self._matrix))
        for i in range(10*size):
            pool.add(GeneticSnakeIndividual.randomIndividual(self._matrix, const=True))
        self._ga = GeneticSnakeGeneticAlgorithm(self._matrix, pool, size)


    def __iterate(self):
        ga = self._ga
        for i in range(self._iterations):
            ga.iteration()
        b = ga.best()
        if b > self._best:
            print('Best individual: (%.2f) %s' % (b.fitness(),b))
            self._best = b

    def up(self):
        pass

    def dn(self):
        pass

    def dp(self):
        if self._dp:
            self._dp = None
            return
        from ga_dpapi import dynamicProgramming as DP
        optsnake = DP(self._matrix)
        self._dp = GeneticSnakeIndividual(self._matrix, individual=optsnake)
        print('OPT (DP): %.2f' % self._dp.fitness())

    def update(self):
        self.__iterate()
        self._model.updateColors(self._matrix)
        self._view.repaint(self._model.matrix(),[])
        self._view.drawOpt(self._ga.best())
        self._view.drawDp(self._dp)
        self._view.drawTopTen(self._ga.topten())

    def run(self, timer=100):
        self._timer.start(timer)
        self._interval = self._timer.interval()

        self._view.abortRequested.connect(self._exit)
        self._view.gameOverRequested.connect(self._exit)
        self._view.upRequested.connect(self.up)
        self._view.dpRequested.connect(self.dp)
        self._view.dnRequested.connect(self.dn)
        self._view.show()
