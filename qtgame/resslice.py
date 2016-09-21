from ert.ecl import EclFile, EclGrid

class ResSlice():
    def __init__(self,grid,rest,step=5):
        self._grid = EclGrid(grid)
        self._rest = EclFile(rest)
        self._step = step

    def soil(self, swat_kw, a_idx):
        if a_idx < 0:
            return 0
        swat = swat_kw[a_idx]
        val = 1.0 - abs(0.7 - swat)
        if swat > 0.7:
            val /= 2
        return val

    def getwall(self, i):
        grid, rest = self._grid, self._rest
        swat_kw = rest.iget_kw('SWAT', 0)[self._step]
        nx, ny, nz = grid.getNX(), grid.getNY(), grid.getNZ()
     
        wall = []
        for j in range(ny):
            c = []
            for k in range(nz):
                ijk = i, j, k
                a = grid.get_active_index(ijk=ijk)
                val = self.soil(swat_kw, a)
                c.append(val)
            if max(c) > 0: # filter out inactive columns
                wall.append(c)
        return wall
