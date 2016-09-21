from snake_model import SnakeModel

class SnakeModelNorne(SnakeModel):
    def __init__(self, res_slice, x=20,y=10):
        self._res = res_slice
        self._i = 0
        self._j = 5
        self._wall = []
        SnakeModel.__init__(self,x,y)

    def nextColumn(self):
        if self._i >= len(self._wall):
            self._wall = self._res.getwall(self._j)
            self._j += 1
            self._i = 0
        c = self._wall[self._i]
        self._i += 1
        return c
