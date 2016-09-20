from __future__ import print_function

from PyQt4.QtGui import QPen, QColor, QBrush

from math import sqrt
from random import random, randint
import colorsys

def ri(x):
    return randint(0,x-1)

def soil(x):
    val = random() + (1-abs(1.5 - x))
    return max(0, min(val, 1))

def heatcolor(val, minval=0, maxval=1):
    h = (float(val-minval) / (maxval-minval)) * 120
    r, g, b = colorsys.hsv_to_rgb(h/360, 1., 1.)
    return QColor.fromRgb(int(r*255), int(g*255), int(b*255))

def colorize(obj, val):
    """Takes and q object and colors it with val"""
    pen,brush = obj.pen(), obj.brush()
    c = heatcolor(val)
    pen.setColor(c)
    brush.setColor(c)
    obj.setPen(pen)
    obj.setBrush(brush)
