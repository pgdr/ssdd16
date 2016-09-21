from ert.ecl import EclFile, EclGrid

class ResSlice():
    def __init__(self,grid,rest,step=5):
        self._grid = EclGrid(grid)
        self._rest = EclFile(rest)
        self._step = step
        self._num_steps = self._rest.num_report_steps()

    def soil(self, swat_kw, a_idx):
        if a_idx < 0:
            return 0
        swat = swat_kw[a_idx]
        val = 1.0 - abs(0.7 - swat)
        if swat > 0.7:
            val /= 2
        return val

    def nextStep(self):
        self._step += 1

    def getwall(self, i):
        grid, rest = self._grid, self._rest
        nx, ny, nz = grid.getNX(), grid.getNY(), grid.getNZ()
        if i >= nx:
            i = 0
            self.nextStep()

        swat_kw = rest.iget_kw('SWAT', 0)[self._step % self._num_steps]
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
