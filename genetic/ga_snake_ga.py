from ga_snake_utils import ri

class GeneticSnakeGeneticAlgorithm():


    def __init__(self, matrix, generator, poolsize=100):
        self._width = len(matrix)
        self._height = len(matrix[0])
        self._matrix = matrix
        self._generator = generator

        self._pool = []
        self._poolsize = poolsize
        self.shake()

    def best(self):
        """Get the current best individual"""
        return self._pool[0]

    def topten(self,n=10):
        """Get top n individuals"""
        ret = []
        p = self._pool
        for i in range(min(n, len(p))):
            ret.append(p[i])
        return ret

    def iteration(self):
        """Do one iteration of crossover and mutation.  Pool is ordered afterwards."""
        p = self._pool
        l = len(p)
        for i in range(0,l,2):
            mother,father = p[i],p[i+1]
            daughter, son = father.crossover(mother), mother.crossover(father)
            p.append(son)
            p.append(daughter)
        l = len(p)
        for i in range(l):
            p.append(p[i].mutate())
        self._pool = set(self._pool)
        self.__order()
        if len(self._pool) > self._poolsize:
            self._pool = self._pool[:self._poolsize]

    def shake(self):
        """Shake.  Generate poolsize many random individuals on top of list."""
        npool = []
        for i in range(self._poolsize):
            npool.append(self._generator(self._matrix))
        npool += self._pool
        self._pool = npool

    def __order(self):
        pool = sorted(self._pool, reverse=True)
        self._pool = pool

    def __str__(self):
        s = "GA:\n"
        p = self._pool
        for ind in p:
            s += '\t%.2f: %s\n' % (ind.fitness(), ind)
        return s
