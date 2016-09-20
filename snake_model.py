from snake_utils import soil, ri, colorize

class SnakeModel():
    def __init__(self, x=20,y=10):
        self._x = x
        self._y = y
        self._grid = []
        for i in range(x):
            c = []
            for j in range(y):
                c.append(ri(10))
            self._grid.append(c)
        self._snake = [(x/2-2, y/2),(x/2-1, y/2),(x/2, y/2)]

    def nextColumn(self):
        c = []
        for i in range(self._y):
            c.append(abs(soil(i/10.0))/5)
        return self._grid.append(c)

    def snakeUp(self):
        i,j = ri(self._x), ri(self._y)
        self._grid[i][j] = soil(0.7)
        print('snake up')

    def snakeDn(self):
        i,j = ri(self._x), ri(self._y)
        self._grid[i][j] = soil(0.3)
        print('snake dn')

    def matrix(self):
        return self._grid
    def snake(self):
        return self._snake

    def updateColors(self,grid):
        height,width=self._y,self._x
        for i in range(0,width-1):
            for j in range(height):
                grid[i][j] = grid[i+1][j]

        col = column(height)
        for i in range(height):
            colorize(grid[width-1][i], col[i])
