from PyQt4.QtGui import QApplication

from snake_game import SnakeGame
from snake_view import SnakeView
from snake_model import SnakeModel

def main():
    height = 20
    width  = 50
    size   = 20
    timer  = 100 # ms sleep

    app = QApplication([])
    view = SnakeView(width, height, size)
    model = SnakeModel(width, height)
    controller = SnakeGame(view, model, app)
    controller.run(timer)

    app.exec_()

if __name__ == '__main__':
    main()
