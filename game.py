from __future__ import print_function
from graphics import *
from time import sleep, time
from random import random, randint

# Should be a game property object
height = 20
width  = 50
size   = 20

TIMELIMIT = 60
TIMEDELAY = 0.1

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
    if random() > 0.80:
        nf.append((width, randint(0, height)))
    return nf


def gameLoop(win):
    global height, width, size, TIMELIMIT, TIMEDELAY
    scoreLabel = Text(Point(2*size,size), "Score: 1")
    scoreLabel.draw(win)
    timeLabel = Text(Point(2*size,2*size+10), "")
    timeLabel.draw(win)

    snake = [(width/2-2, height/2),(width/2-1, height/2),(width/2, height/2)]
    sprite = []
    flies = []
    fliesSprite = []
    grow = False
    current = height/2
    playtime = time()
    while True:
        scoreLabel.setText('Score: %d' % len(snake))
        timeLabel.setText('%d' % round(TIMELIMIT - (time() - playtime)))
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
        if len(snake) == width / 2:
            return True
        if time() - playtime > TIMELIMIT:
            return False
        sleep(TIMEDELAY)
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



