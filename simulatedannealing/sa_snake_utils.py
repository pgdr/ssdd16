from __future__ import print_function

from PyQt4.QtGui import QPen, QColor, QBrush

from math import sqrt
from random import random, randint
import colorsys

def soil(x):
    val = (1.0 - abs(0.7 - x))
    val += random() - 0.5 # in [-0.5, 0.5]
    return max(0, min(val, 1))

def ri(x):
    return randint(0,x-1)

def heatcolor(val, minval=0, maxval=1):
    h = (float(val-minval) / (maxval-minval)) * 120
    r, g, b = colorsys.hsv_to_rgb(h/360, 1., 1.)
    return QColor.fromRgb(int(r*255), int(g*255), int(b*255))

def colorize(obj, val):
    """Takes and q object and colors it with val"""
    pen,brush = obj.pen(), obj.brush()
    if val == 2:
        c = QColor.fromRgb(0,0,255)
    else:
        c = heatcolor(val)
    pen.setColor(c)
    brush.setColor(c)
    obj.setPen(pen)
    obj.setBrush(brush)

def addToSnake(snake, head, grow=False):
    snake.append(head)
    ns = []
    start = 1
    if grow:
        start = 0
    for i in range(start,len(snake)):
        ns.append((snake[i][0]-1, snake[i][1]))
    return ns
