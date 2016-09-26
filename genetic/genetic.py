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
    print('')
    print('Press Q/Esc  to quit')

def main():
    height = 20
    width  = 30
    size   = 14
    timer  = 15 # ms sleep

    iters    = 1  # GA iterations per update
    poolsz   = 80 # GA pool size (apx, will vary)
    numlines = 80 # number of lines to draw (e.g. top 10 best individ)
    apxratio = 0.99

    printIntro()
    if len(sys.argv) != 2:
        print('Provide matrix file')
        exit(1)

    matrix = readMatrix()
    width = len(matrix)
    height= len(matrix[0])
    app = QApplication([])
    view = GeneticSnakeView(width, height, size)
    model = GeneticSnakeModel(width, height)
    controller = GeneticSnakeGame(view, model, app.quit, matrix, iters, poolsz, apxratio, numlines=numlines)
    controller.run(timer)

    app.exec_()






def readMatrix():
    mfile = sys.argv[1]
    first = True
    matrix = []
    with open(mfile, 'r') as f:
        for line in f:
            data = map(float, line.strip().split())
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
