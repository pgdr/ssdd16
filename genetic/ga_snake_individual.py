import math
from ga_snake_utils import ri
from random import random, randint

class GeneticSnakeIndividual():

    def __init__(self, matrix):
        self._width = len(matrix)
        self._height = len(matrix[0])
        self._matrix = matrix
        self._snake = []
        self._fitness = None

    def __computeFitness(self):
        s = self._snake
        try:
            self._fitness = sum([self._matrix[i][s[i]] for i in range(len(s))])
        except IndexError:
            print(s)
            raise IndexError(str(s))

    def __freeze(self):
        self._snake = tuple(self._snake)
        self.__computeFitness()
        assert(self.__isvalid())

    def __unfreeze(self):
        self._snake = list(self._snake)
        self._fitness = None
        assert(self.__isvalid())

    def __propagateLeft(self, idx):
        if idx <= 0:
            return
        s = self._snake
        vl,vr = s[idx-1], s[idx] # left,right
        if vl < vr:
            s[idx-1] = vr - 1
        elif vl > vr:
            s[idx-1] = vr + 1
        self.__propagateLeft(idx-1)

    def __propagateRight(self, idx):
        if idx >= self._width-1:
            return
        s = self._snake
        vl,vr = s[idx], s[idx+1] # left,right
        if vl < vr:
            s[idx+1] = vl + 1
        elif vl > vr:
            s[idx+1] = vl - 1
        self.__propagateRight(idx+1)

    def __isvalid(self):
        s = self._snake
        if len(s) != self._width:
            print('Snake wrong length: %d vs %s' % (self._width, s))
            return False
        for i in range(1, self._width):
            if abs(s[i-1] - s[i]) > 1:
                print("Differ error")
                return False
            if not 0 <= s[i-1] < self._height:
                print("Out of range idx=%d: 0 <= %d < %d" % (i-1, s[i-1], self._height))
                return False
            if not 0 <= s[i] < self._height:
                print("Out of range idx=%d: 0 <= %d < %d" % (i, s[i], self._height))
                return False
        return True


    def fitness(self):
        if self._fitness is None:
            self.__computeFitness()
        return self._fitness

    def __mutateline(self):
        m = GeneticSnakeIndividual(self._matrix)
        m._snake = [self._snake[i] for i in range(self._width)]
        ud = randint(-1,1)
        for i in range(len(self._snake)):
            m._snake[i] = m.__ysqueeze(self._snake[i] + ud)
        m.__freeze()
        return m


    def __mutatepoint(self):
        m = GeneticSnakeIndividual(self._matrix)
        m._snake = [self._snake[i] for i in range(self._width)]
        e = ri(self._width)
        ud = randint(-1,1)
        m._snake[e] = self.__ysqueeze(m._snake[e] + ud)
        if e > 0:
            m.__propagateLeft(e)
        if e < self._width - 1:
            m.__propagateRight(e)
        m.__freeze()
        return m

    def mutate(self):
        assert(self.__isvalid())
        m = None
        if random() <= 0.33:
            m = self.__mutatepoint()
        else:
            m = self.__mutateline()
        assert(m.__isvalid())
        return m

    def crossover(self, other):
        assert(self.__isvalid())
        assert(other.__isvalid())
        m = self.mutate()
        m.__unfreeze()
        c = ri(m._width)
        for i in range(c, m._width):
            m._snake[i] = other._snake[i]
        m.__propagateRight(0)
        m.__freeze()
        assert(m.__isvalid())
        return m

    def __str__(self):
        return 'Snake: %s' % str(self._snake)
    def __len__(self):
        return len(self._snake)
    def __getitem__(self, idx):
        return self._snake[idx]
    def __eq__(self, other):
        return self._snake == other._snake
    def __ne__(self, other):
        return self._snake != other._snake

    def __hash__(self):
        return hash(self._snake)

    def __ysqueeze(self, y):
        if y >= self._height:
            return self._height-1
        if y < 0:
            return 0
        return y

    def __squeeze(self):
        self.__unfreeze()
        for i in range(self._width):
            self._snake[i] = self.__ysqueeze(self._snake[i])
        self.__freeze()

    def __le__(self, other):
        return self.fitness() <= other.fitness()
    def __lt__(self, other):
        return self.fitness() < other.fitness()
    def __ge__(self, other):
        return self.fitness() >= other.fitness()
    def __gt__(self, other):
        return self.fitness() > other.fitness()

    @staticmethod
    def randomIndividual(matrix, const=False):
        width = len(matrix)
        height = len(matrix[0])
        s = GeneticSnakeIndividual(matrix)
        s._snake.append(ri(height))
        for i in range(1,width):
            ud = randint(-1,1)
            if const:
                ud = 0
            y = s._snake[i-1] + ud
            s._snake.append(s.__ysqueeze(y))
        s.__freeze()
        assert(s.__isvalid())
        return s
