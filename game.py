from __future__ import print_function
from graphics import *
from time import sleep
import sys
from random import random, randint

mx = []
with open(sys.argv[1], 'r') as f:
    for l in f:
        l = l.strip()
        if len(l) > 0:
            mx.append(map(float, l.split()))


height = 50
width  = 100
size   = 10

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
        b.setFill('red')
        b.draw(win)
        sprite.append(b)
    return sprite

def drawFlies(win, flies, fliesSprite):
    for s in fliesSprite:
        s.undraw()
    fs = []
    for i in range(len(flies)):
        f = sq(flies[i][0], flies[i][1])
        f.setFill('green')
        f.draw(win)
        fs.append(f)
    return fs
        

def hit(snake, flies):
    for i in range(len(flies)):
        if flies[i] == snake[0]:
            return i
    return -1
    
def updateFlies(flies):
    nf = []
    for f in flies:
        if f[0] > 0:
            nf.append((f[0]-1,f[1]))
    if random() > 0.93:
        nf.append((width, randint(0, height)))
    return nf


def gameLoop(win):
    global height, width, size
    snake = [(width/2, height/2)]
    sprite = []
    flies = []
    fliesSprite = []
    grow = False
    current = height/2
    while True:
        flies = updateFlies(flies)
        fliesSprite = drawFlies(win, flies, fliesSprite)
        hit_idx = hit(snake, flies)
        grow = hit_idx >= 0
        if grow:
            flies = flies[:hit_idx] + flies[hit_idx+1:]
        
        sprite = drawSnake(win, snake, sprite)
        k = win.checkKey()
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
            print('Flies: %s' % str(flies))


        snake = addToSnake(snake, current, grow=grow)
        sleep(0.1)
    

def main():
    global height, width, size
    win = GraphWin("Snakewell", width=width*size, height=height*size)
    gameLoop(win)
    win.close()    # Close window when done




main()



