import os

from PyQt5 import QtWidgets, uic

from app.controller import Controller
from app.shapes_store import ShapesStore
from app.shapes import Rectangle, Dot, Line, Circle
from app.utils import Point


def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    current_dir = os.path.dirname(__file__)
    with open(current_dir + '/ui/mainWindow.ui') as f:
        uic.loadUi(f, window)

    # Here we choose, which printer we want to create and use
    controller = Controller()

    # If we choose CanvasPrinter, we must also add it to the canvasArea in the main window as a widget
    canvas_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')
    canvas_area.setWidget(controller.canvas)
    window.show()

    return app.exec()
