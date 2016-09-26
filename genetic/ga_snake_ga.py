from ga_snake_utils import ri

class GeneticSnakeGeneticAlgorithm():


    def __init__(self, matrix, pool, size=100):
        self._width = len(matrix)
        self._height = len(matrix[0])
        self._matrix = matrix
        self._pool = []
        self._size = size

        p = self._pool
        for ind in pool:
            p.append(ind)
        l = len(p)
        while l < size:
            p.append(p[ri(l)].mutate())
            l = len(p)

    def best(self):
        return self._pool[0]

    def topten(self,n=10):
        ret = []
        p = self._pool
        for i in range(max(n, len(p))):
            ret.append(p[i])
        return ret

    def iteration(self):
        p = self._pool
        l = len(p)
        for i in range(l):
            p.append(p[i].mutate())
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
        if self._pool > self._size:
            self._pool = self._pool[:self._size]

    def __order(self):
        pool = sorted(self._pool, reverse=True)
        self._pool = pool

    def __str__(self):
        s = "GA:\n"
        p = self._pool
        for ind in p:
            s += '\t%.2f: %s\n' % (ind.fitness(), ind)
        return s
