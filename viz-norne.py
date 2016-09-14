from __future__ import print_function
import sys
import colorsys
from graphics import *
from time import sleep
from dpapi import dynamicProgramming

import resslice

def pseudocolor(val, minval=0.0, maxval=1.0):
    h = (float(val-minval) / (maxval-minval)) * 120
    r, g, b = colorsys.hsv_to_rgb(h/360, 1., 1.)
    return r*255, g*255, b*255

if len(sys.argv) < 2:
    print('Usage: viz-norne i')
    exit(1)

i = int(sys.argv[1])

wall = resslice.getwall(i)
mx = []
nz = len(wall[0])
ny = len(wall)
for k in range(nz):
    row = [wall[i][k] for i in range(ny)]
    mx.append(row)

n = len(mx)
m = len(mx[0])

height = n
width  = m
size   = 20

def thickLine(p1,p2):
    global size
    eps = int(round(size/10.0 + 1))
    p1u = Point(p1.x, p1.y-eps)
    p1d = Point(p1.x, p1.y+eps)
    p2u = Point(p2.x, p2.y-eps)
    p2d = Point(p2.x, p2.y+eps)
    polygone = [p1d,p1u,p2u,p2d,p1d]
    p = Polygon(polygone)
    p.setFill('black')
    p.setOutline('black')
    return p

def sq(x, y, val, chosen=False):
    global size
    col = pseudocolor(val)
    p1 = Point(x*size, y*size)
    p2 = Point((x+1)*size, (y+1)*size)
    rec = Rectangle(p1,p2)
    rec.setFill(color_rgb(*col))
    if chosen:
        rec.setOutline('white')
    return rec

def drawSnake(win, snake, sprite=None):
    if sprite:
        for s in sprite:
            s.undraw()
    global size
    t = size/2
    sprite = []
    for i in range(1,len(snake)):
        x1,y1 = i-1, snake[i-1]
        x2,y2 = i,   snake[i]
        p1 = Point(x1*size+t,y1*size+t)
        p2 = Point(x2*size+t,y2*size+t)
        l = thickLine(p1,p2)
        l.draw(win)
        sprite.append(l)
    return l
        


def main():
    global m,n,mx,height,width,size
    snake = dynamicProgramming(mx)
    win = GraphWin("Snakewell", width=width*size, height=height*size)
    for i in range(m):
        for k in range(n):
            r = sq(i,k, mx[k][i])
            r.draw(win)
    drawSnake(win, snake)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done


main()
