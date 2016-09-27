from math import sqrt
class SimulatedSnakeSimulatedAnnealing():

    def __init__(self, matrix, generator, temperature=100):
        self._width = len(matrix)
        self._height = len(matrix[0])
        self._matrix = matrix
        self._sol = generator(matrix)
        self._temperature = temperature
        self._prev_attempts = [self._sol]

    def best(self):
        """Get the current best individual"""
        return self._sol

    def prev(self):
        return self._prev_attempts

    def __addPrev(self, n):
        self._prev_attempts.append(n)
        if len(self._prev_attempts) > 10:
            self._prev_attempts = self._prev_attempts[-10:]

    def accept(self, new, old):
        """Returns true if we should accept the new energy level"""
        if new > old:
            return True
        return (old - new) < self._temperature

    def iteration(self):
        """Do one iteration of crossover and mutation.  Pool is ordered afterwards."""
        t = self._temperature
        
        s = self._sol
        es = s.fitness() # energy old individual

        n = s.mutate()
        en = n.fitness() # energy new individual

        self.__addPrev(n)

        if self.accept(en, es):
            self._sol = n
        self._temperature = t / 1.005

    def __str__(self):
        return "SA: %s" % str(self._sol)
