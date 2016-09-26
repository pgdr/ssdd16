from PyQt4.QtCore import QTimer

from time import time
from math import sqrt

from ga_snake_individual import GeneticSnakeIndividual
from ga_snake_ga import GeneticSnakeGeneticAlgorithm

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
        self._iterations = iterations
        self._poolsize = poolsize
        self._numlines = numlines # draw the top n best as lines
        self._ga = GeneticSnakeGeneticAlgorithm(self._matrix, GeneticSnakeIndividual.randomIndividual, poolsize)
        self._best = self._ga.best()
        self._best_repeated = 0
        self._optlimit = optlimit
        self._optsnake = self.__dpsnake()
        self._opt = self._optsnake.fitness()
        self._drawn = False

    def __dpsnake(self):
        optsnake = DP(self._matrix)
        return GeneticSnakeIndividual(self._matrix, individual=optsnake)


    def __iterate(self):
        ga = self._ga
        for i in range(self._iterations):
            ga.iteration()
        b = ga.best()
        if b > self._best:
            print('Best individual: (%.2f) %s' % (b.fitness(),b))
            self._best = b
            if b.fitness() >= self._opt * self._optlimit:
                print('Reached %d%% of opt.  Exit.' % int(100.0*self._optlimit))
                self._exit()
        else:
            self._best_repeated += 1
            if self._best_repeated > 25:
                print("SHAAAAAKE IT UP!!!")
                self._ga.shake()
                self._best_repeated = 0

    def dp(self):
        if self._dp:
            self._dp = None
            return
        self._dp = self._optsnake
        print('OPT (DP): %.2f' % self._dp.fitness())

    def update(self):
        self.__iterate()
        self._model.updateColors(self._matrix)
        if not self._drawn:
            self._view.repaint(self._model.matrix(),[])
            self._drawn = True
        self._view.drawOpt(self._ga.best())
        self._view.drawDp(self._dp)
        self._view.drawTopTen(self._ga.topten(self._numlines))

    def run(self, timer=100):
        self._timer.start(timer)
        self._interval = self._timer.interval()

        self._view.abortRequested.connect(self._exit)
        self._view.gameOverRequested.connect(self._exit)
        self._view.dpRequested.connect(self.dp)
        self._view.show()
