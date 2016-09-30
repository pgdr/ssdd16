#!/usr/bin/env python

from __future__ import print_function
from PyQt4.QtGui import QApplication
import sys
from sa_snake_game import SimulatedSnakeGame
from sa_snake_view import SimulatedSnakeView
from sa_snake_model import SimulatedSnakeModel

from sa_snake_individual import SimulatedSnakeIndividual
from sa_snake_sa import SimulatedSnakeSimulatedAnnealing

def printIntro():
    print('Welcome  to  SnakeGene!')
    print('')
    print('Usage:       simulated.py matrix.m')
    print('Usage:       simulated.py bigmatrix.m')
    print('Usage:       simulated.py ~/norne/NORNE_ATW2013.EGRID')
    print('Usage:       simulated.py ~/norne/NORNE_ATW2013.EGRID 11')
    print('')
    print('Press Space  to show OPT (DP)')
    print('Press Q/Esc  to quit')


def main():
    size   = 10 # drawn size of each cell
    timer  = 15 # ms sleep

    iters    = 100  # iterations per update
    temp     = 10 # temperature
    apxratio = 0.99

    printIntro()
    if len(sys.argv) < 2:
        print('Provide matrix or EGRID file.')
        exit(1)

    fname = sys.argv[1]
    matrix = None
    if fname[-6:] == '.EGRID':
        i_slice = 11
        if len(sys.argv) == 3:
            i_slice = int(sys.argv[2])
        matrix = readGrid(fname, i_slice)
        if not matrix:
            print('Failed to read ecl files.')
            exit(1)
    else:
        matrix = readMatrix(fname)

    width = len(matrix)
    height= len(matrix[0])

    app = QApplication([])
    view = SimulatedSnakeView(width, height, size)
    model = SimulatedSnakeModel(width, height)
    controller = SimulatedSnakeGame(view, model, app.quit, matrix, iters, temp, apxratio)
    controller.run(timer)

    app.exec_()




def readGrid(fname, i_slice):
    try:
        from ert.ecl import EclGrid, EclFile
        from resslice import getwall
        from os.path import isfile
        initfname = fname[:-6] + '.INIT'
        restfname = fname[:-6] + '.UNRST'
        init,rest = None, None
        if isfile(restfname):
            rest = EclFile(restfname)
        elif isfile(initfname):
            init = EclFile(initfname)
        else:
            print('Need at least one of INIT and UNRST.')
            return None
        grid = EclGrid(fname)
        return getwall(i_slice, grid, init, rest)
    except Exception as e:
        print(e)
        return None

def readMatrix(fname):
    first = True
    matrix = []
    with open(fname, 'r') as f:
        for line in f:
            data = list(map(float, line.strip().split()))
            for i in range(len(data)):
                r = data[i]
                if first:
                    matrix.append([r])
                else:
                    matrix[i].append(r)
            first = False
    return matrix



if __name__ == '__main__':
    main()
