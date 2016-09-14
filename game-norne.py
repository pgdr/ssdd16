from __future__ import print_function
from graphics import *
from time import sleep, time
import sys
from random import random, randint
import colorsys

import resslice

# Should be a game property object
height = 22 # norne happens to be 22 high
width  = 40
size   = 40

TIMELIMIT = 6000
TIMEDELAY = 0.01



##############################
# COLOR

def pseudocolor(val, minval=0, maxval=1):
    h = (float(val-minval) / (maxval-minval)) * 120
    r, g, b = colorsys.hsv_to_rgb(h/360, 1., 1.)
    return r*255, g*255, b*255

def soil(x):
    return random() + (1-abs(1.5 - x))

def transpose(mx):
    out_mx = []
    for idx in range(len(mx)):
        col = [mx[idx][jdx] for jdx in range(len(mx[idx]))]
        out_mx.append(col)
    return out_mx

slice_idx = 16
wall = []

def column(size):
    global wall,slice_idx
    if len(wall) == 0:
        mx = resslice.getwall(slice_idx)
        wall = transpose(mx)
        slice_idx += 1
        print(slice_idx)
    col = wall[-1]
    wall = wall[:-1]
    print(len(wall))
    return col
        
        

def colorize(obj, val):
    obj.setFill(color_rgb(*pseudocolor(val)))

def updateColors(grid):
    global height,width
    for i in range(0,width-1):
        for j in range(height):
            grid[i][j].setFill(grid[i+1][j].getFill())

    col = column(height)
    for i in range(height):
        colorize(grid[width-1][i], col[i])


#########################################
#                GAME
#########################################

def addToSnake(snake, e, grow=False):
    snake.append((width/2 + 1, e))
    ns = []
    start = 1
    if grow:
        start = 0
    for i in range(start,len(snake)):
        ns.append((snake[i][0]-1, snake[i][1]))
    return ns

def sq(x, y):
    global size
    p1 = Point(x*size, y*size)
    p2 = Point((x+1)*size, (y+1)*size)
    return Rectangle(p1,p2)

def drawSnake(win, snake, sprite):
    global width
    for e in sprite:
        e.undraw()
    sprite = []
    ls = len(snake) # number of points! :D
    for i in range(ls):
        b = sq(snake[i][0], snake[i][1])
        b.setFill('blue')
        b.draw(win)
        sprite.append(b)
    return sprite

def gameLoop(win):
    global height, width, size, TIMELIMIT, TIMEDELAY
    scoreLabel = Text(Point(2*size,size), "Score: 1")
    scoreLabel.draw(win)
    score = 0
    timeLabel = Text(Point(2*size,2*size+10), "")
    timeLabel.draw(win)

    snake = [(width/2-2, height/2),(width/2-1, height/2),(width/2, height/2)]
    sprite = []
    grow = False
    current = height/2
    playtime = time()
    grid = []
    for i in range(width):
        grid.append([])
        col = column(height)
        for j in range(height):
            r = sq(i,j)
            colorize(r, col[j])
            r.draw(win)
            grid[i].append(r)

    while True:
        scoreLabel.setText('Score: %.2f' % score)
        timeLabel.setText('%d' % round(TIMELIMIT - (time() - playtime)))
        sprite = drawSnake(win, snake, sprite)
        k = win.checkKey()
        if score/10.0 > len(snake):
            grow = True
        if k == 'q':
            print('quit')
            break
        if k == 'w':
            print('up')
            current -= 1
        if k == 's':
            current += 1
            print('dw')
        if k == 'h':
            grow = True
            print('hit')
        if k == 'l':
            print('Snake: %s' % str(snake))

        
        snake = addToSnake(snake, current, grow=grow)
        if len(snake) == width / 2:
            return True
        if time() - playtime > TIMELIMIT:
            return False
        sleep(TIMEDELAY)
        # Color
        updateColors(grid)
        # sooo many levels of you don't wanna know!!!
        hx = int('00' + grid[width/2][snake[0][1]].getFill()[3:],16)
        hx = hx / 100000.0
        score += hx
        print('score: %.2f' % score)
        grow = False
    return False


def main():
    global height, width, size, TIMELIMIT
    win = GraphWin("Snakewell", width=width*size, height=height*size)
    start = time()
    if gameLoop(win):
        stop = time()
        diff = round(stop-start,2)
        print('New high score! %d' % (TIMELIMIT-diff))
    else:
        print('Loser')
    win.close()    # Close window when done




main()



