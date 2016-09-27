import sys

def soil(kw, a_idx):
    if a_idx < 0:
        return 0
    swat = kw[a_idx]
    val = 1.0 - abs(0.7 - swat)
    if swat > 0.7:
        val /= 2
    return val

def getwall(i_slice, grid, init=None, rest=None, rest_step=5):
    if init is None and rest is None:
        raise ValueError('At least one of init and rest must be set')

    if rest:
        kw = rest.iget_kw('SWAT', 0)[rest_step]
    else:
        kw = init.iget_kw('SWATINIT', 0)[0]
    nx,ny,nz = grid.getNX(),grid.getNY(),grid.getNZ()

    wall = []
    for j in range(ny):
        c = []
        for k in range(nz):
            ijk = i_slice, j, k
            a = grid.get_active_index(ijk=ijk)
            val = soil(kw, a)
            c.append(val)
        if max(c) > 0:
            wall.append(c)
    if len(wall) == 0:
        raise ValueError('Slice %d is inactive.' % i_slice)
    return wall
