#!/usr/bin/env python

from __future__ import print_function
from PyQt4.QtGui import QApplication
import sys
from ga_snake_game import GeneticSnakeGame
from ga_snake_view import GeneticSnakeView
from ga_snake_model import GeneticSnakeModel

from ga_snake_individual import GeneticSnakeIndividual
from ga_snake_ga import GeneticSnakeGeneticAlgorithm

def printIntro():
    print('Welcome  to  SnakeGene!')
    print('')
    print('Usage:       genetic.py matrix.m')
    print('Usage:       genetic.py bigmatrix.m')
    print('Usage:       genetic.py ~/norne/NORNE_ATW2013.EGRID')
    print('Usage:       genetic.py ~/norne/NORNE_ATW2013.EGRID 11')
    print('')
    print('Press Space  to show OPT (DP)')
    print('Press Q/Esc  to quit')


def main():
    size   = 14 # drawn size of each cell
    timer  = 15 # ms sleep

    iters    = 1  # GA iterations per update
    poolsz   = 80 # GA pool size (apx, will vary)
    numlines = 80 # number of lines to draw (e.g. top 10 best individ)
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
    view = GeneticSnakeView(width, height, size)
    model = GeneticSnakeModel(width, height)
    controller = GeneticSnakeGame(view, model, app.quit, matrix, iters, poolsz, apxratio, numlines=numlines)
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
