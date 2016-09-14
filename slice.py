from ert.ecl import EclFile, EclGrid
import sys

def soil(swat_kw, a_idx):
    if a_idx < 0:
        return 0
    swat = swat_kw[a_idx]
    return 1 - abs(0.7 - swat)

def getwall(i):
    gridfile = 'norne/NORNE_ATW2013.EGRID'
    initfile = 'norne/NORNE_ATW2013.INIT'
    restfile = 'norne/NORNE_ATW2013.UNRST'
     
    grid = EclGrid(gridfile)
    init = EclFile(initfile)
    rest = EclFile(restfile)
     
    swat_kw = rest.iget_kw('SWAT', 0)[0]
    nx,ny,nz = grid.getNX(),grid.getNY(),grid.getNZ()
     
    wall = []
    for j in range(ny):
        c = []
        for k in range(nz):
            ijk = i, j, k
            a = grid.get_active_index(ijk=ijk)
            val = soil(swat_kw, a)
            c.append(val)
        wall.append(c)
    return wall

def main():
    if len(sys.argv) != 2:
        print('Usage: slice i')
        print('       slice 11')
        print('       slice 16')
        exit(0)

    i = 0
    try:
        i = int(sys.argv[1])
    except:
        print('Usage: slice i')
        exit()

    wall = getwall(i)
    nz = len(wall[0])
    ny = len(wall)
    for k in range(nz):
        row = ['%.2f' % wall[i][k] for i in range(ny)]
        row_str = ' '.join(row)
        print(row_str)

if __name__ == '__main__':
    main()
