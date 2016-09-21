from snake_utils import soil, ri, colorize, addToSnake

class SnakeModel():
    def __init__(self, x=20,y=10):
        self._x = x
        self._y = y
        self.__setup__()
        self._current = y/2 # head of snake
        self._grow = False # should snake grow next iteration?

    def __setup__(self):
        x,y = self._x, self._y
        self._grid = []
        for i in range(x):
            c = self.nextColumn()
            self._grid.append(c)
        self._snake = [(x/2-2, y/2),(x/2-1, y/2),(x/2, y/2)]

    def width(self):
        return self._x
    def height(self):
        return self._y


    def nextColumn(self):
        h = float(self.height())
        c = []
        for i in range(self.height()):
            s = abs(soil(i/h))
            c.append(s)
        return c

    def snakeHeadValue(self):
        i,j = self.snakeHead()
        return self._grid[i][j]

    def snakeHead(self):
        return self._snake[0]

    def snakeGrow(self, grow=True):
        self._grow = grow

    def snakeUp(self):
        self._current = max(0, self._current - 1)

    def snakeDn(self):
        self._current = min(self.height()-1, self._current + 1)

    def matrix(self):
        return self._grid
    def snake(self):
        return self._snake

    def updateColors(self):
        head = (self._x/2, self._current)
        self._snake = addToSnake(self._snake, head, self._grow)
        self._grow = False
        c = self.nextColumn()
        self._grid.append(c)
        self._grid = self._grid[1:]
