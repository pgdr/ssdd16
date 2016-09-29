from PyQt4.QtCore import QEvent, pyqtSignal, QRect, Qt
from PyQt4.QtGui import QPen, QColor, QBrush
from PyQt4.QtGui import QGraphicsScene, QGraphicsView

from ga_snake_utils import colorize

class GeneticSnakeView(QGraphicsView):

    gameOverRequested = pyqtSignal()
    abortRequested    = pyqtSignal()
    dpRequested       = pyqtSignal() # Toggle DP
    BLACK = QColor.fromRgb(  0,   0,   0)
    BLUE  = QColor.fromRgb(  0,   0, 255)
    WHITE = QColor.fromRgb(255, 255, 255)
    GRAY  = QColor.fromRgb(100, 100, 100)

    def __init__(self, width, height, size=10):
        super(GeneticSnakeView, self).__init__()
        self._keymap = {Qt.Key_Q:      self.abortRequested,
                        Qt.Key_Escape: self.abortRequested,
                        Qt.Key_Space:  self.dpRequested}
        self._width = width   # no squares wide (i/x/m direction)
        self._height = height # no squares high (j/y/n direction)
        self._size = size     # pixels per square, e.g. 10x10
        self._grid = []
        self.__setup__()
        self._scoreItem = self.scene.addSimpleText('')
        self._prevOpt = []
        self._prevTopTens = []
        self._prevDp = []

    def _text(self, text, x, y, pen=None, brush=None, shrink=False):
        if not pen:
            pen = self._pen
        if not brush:
            brush = self._brush
        ss = self._size
        t = self.scene.addSimpleText(text)
        t.setPos(x*ss + ss/10.0, y*ss + ss/10.0)
        return t


    def _sq(self, x, y, pen=None, brush=None, shrink=False):
        if not pen:
            pen = self._pen
        if not brush:
            brush = self._brush
        ss = self._size
        quad = x*ss, y*ss, ss, ss
        if shrink:
            quad = x*ss+3, y*ss+3, ss-6, ss-6
        rect = self.scene.addRect(*quad,
                                  pen=pen, brush=brush)
        return rect

    def __setup__(self):
        self._pen = QPen(GeneticSnakeView.BLACK)
        self._brush = QBrush(GeneticSnakeView.BLACK)
        self._pen.setWidth(1)
        x,y=(1+self._width) * self._size, (1+self._height) * self._size
        self.setGeometry(QRect(0,0,x,y))
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.installEventFilter(self)

        for i in range(self._width):
            self._grid.append([])
            for j in range(self._height):
                r = self._sq(i,j)
                self._grid[i].append(r)

    def eventFilter(self, obj, event):
        """We catch and absorb all key presses"""
        if event.type() == QEvent.KeyPress:
            k = event.key()
            if k in self._keymap:
                self._keymap[k].emit()
            return True
        else:
            return False

    def repaint(self, matrix, snake):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                val = matrix[i][j]
                colorize(self._grid[i][j], val)

    def drawDp(self, snake):
        for r in self._prevDp:
            self.scene.removeItem(r)
        self._prevDp = []
        if snake is None:
            return
        s = self._size
        p = self._pen
        b = QBrush() # transparent brush
        p.setWidth(2)
        p.setColor(GeneticSnakeView.BLUE)
        for i in range(len(snake)):
            x,y = i, snake[i]
            l =  self._sq(x,y,pen=p,brush=b,shrink=False)
            self._prevDp.append(l)
        p.setWidth(1)

    def drawDpt(self, dpt):
        s = self._size
        p = self._pen
        b = QBrush() # transparent brush
        p.setWidth(2)
        p.setColor(GeneticSnakeView.BLUE)
        for i in range(len(dpt)):
            for j in range(len(dpt[i])):
                text = '%.1f' % dpt[i][j]
                l =  self._text(text,i,j,pen=p,brush=b,shrink=False)
        p.setWidth(1)
