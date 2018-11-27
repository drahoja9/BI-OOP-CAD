import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QColor

from app.drawers import Canvas
from app.shapes import Rectangle, Dot, Line, Circle
from app.utils import Point


def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    current_dir = os.path.dirname(__file__)
    with open(current_dir + '/ui/mainWindow.ui') as f:
        uic.loadUi(f, window)

    canvas_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')
    canvas = Canvas()
    canvas_area.setWidget(canvas)

    r1 = Rectangle(Point(10, 10), 200, 100, QColor(200, 0, 0))
    r2 = Rectangle(Point(100, 100), 20, 10, QColor(0, 200, 0))
    r3 = Rectangle(Point(400, 100), 50, 250, QColor(0, 0, 200))

    dot = Dot(Point(400, 400), QColor(10, 10, 10))

    line = Line(Point(0, 0), Point(953, 551), QColor(0, 0, 250))

    circle = Circle(Point(700, 50), 300, QColor(0, 250, 0))

    canvas.add_shapes(r1, r2, r3, dot, line, circle)

    window.show()

    return app.exec()
