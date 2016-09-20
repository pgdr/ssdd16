from __future__ import print_function
import sys

import threading

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QColor, QBrush

from time import sleep, time
from random import random, randint

# Should be a game property object
height = 20
width  = 50
size   = 40

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
    #QT p1 = Point(x*size, y*size)
    #QT p2 = Point((x+1)*size, (y+1)*size)
    #QT return Rectangle(p1,p2)

def drawSnake(win, snake, sprite):
    global width
    for e in sprite:
        #QT e.undraw()
        pass
    sprite = []
    ls = len(snake) # number of points! :D
    for i in range(ls):
        b = sq(snake[i][0], snake[i][1])
        #QT b.setFill('red')
        # QT b.draw(win)
        sprite.append(b)
    return sprite

def drawFlies(win, flies, fliesSprite):
    for s in fliesSprite:
        # QT s.undraw()
        pass
    fs = []
    for i in range(len(flies)):
        f = sq(flies[i][0], flies[i][1])
        #QT f.setFill('green')
        #QT f.draw(win)
        #QT fs.append(f)
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
    #QT scoreLabel = Text(Point(2*size,size), "Score: 1")
    #QT scoreLabel.draw(win)
    #QT timeLabel = Text(Point(2*size,2*size+10), "")
    #QT timeLabel.draw(win)

    snake = [(width/2-2, height/2),(width/2-1, height/2),(width/2, height/2)]
    sprite = []
    flies = []
    fliesSprite = []
    grow = False
    current = height/2
    playtime = time()
    while True:
        #QT scoreLabel.setText('Score: %d' % len(snake))
        #QT timeLabel.setText('%d' % round(TIMELIMIT - (time() - playtime)))
        flies = updateFlies(flies)
        #QT fliesSprite = drawFlies(win, flies, fliesSprite)
        hit_idx = hit(snake, flies)
        grow = hit_idx >= 0
        if grow:
            flies = flies[:hit_idx] + flies[hit_idx+1:]
        
        sprite = drawSnake(win, snake, sprite)
        #QT k = win.checkKey()
        k = ''
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
    #global height, width, size, TIMELIMIT
    app = QtGui.QApplication([])
    graphicsView = QtGui.QGraphicsView()
     
    graphicsView.setGeometry(QtCore.QRect(0,0,1000,500))
    graphicsView.scene = QtGui.QGraphicsScene(graphicsView)
    graphicsView.setScene(graphicsView.scene)
     
    rg = QColor.fromRgb(0,0,0)
    pen = QPen(rg)
    pen.setWidth(1)
    
    rects = []
    ri = lambda x: randint(0,x-1)

    for i in range(20):
        pen.setColor(QColor.fromRgb(ri(255),ri(255),ri(255)))
        rects.append(graphicsView.scene.addRect(30*i,10*i,10,10,pen))

    def repaint():
        c_r = rects[ri(20)]
        pen.setColor(QColor.fromRgb(ri(255),ri(255),ri(255)))
        c_r.setPen(pen)
        if ri(10) == 5:
            print('paint')

    def stopped_painting():
        print('stopped painting')

    timer = QtCore.QTimer()
    timer.timeout.connect(repaint)
    timer.start(10)


    #life = QtCore.QTimer()
    #life.timeout.connect(painter.stop)
    #life.timeout.connect(stopped_painting)
    #life.setSingleShot(True)
    #life.start(5000)

    graphicsView.show()
    app.exec_()

 
    #start = time()
    #if gameLoop(app):
    #    stop = time()
    #    diff = round(stop-start,2)
    #    print('New high score! %d' % (TIMELIMIT-diff))
    #else:
    #    print('Loser')
    #app.close()    # Close window when done
 
 
 
if __name__ == '__main__':
    main()

