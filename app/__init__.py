import os

from PyQt5 import QtWidgets, uic

from app.main_loop import MainLoop
from app.shapes_store import ShapesStore
from app.printers import CanvasPrinter, TextPrinter, FilePrinter
from app.shapes import Rectangle, Dot, Line, Circle
from app.utils import Point


def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    current_dir = os.path.dirname(__file__)
    with open(current_dir + '/ui/mainWindow.ui') as f:
        uic.loadUi(f, window)

    # Here we choose, which printer we want to create and use
    canvas = CanvasPrinter()
    main_loop = MainLoop(canvas)

    # If we choose CanvasPrinter, we must also add it to the canvasArea in the main window as a widget
    canvas_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')
    canvas_area.setWidget(canvas)
    window.show()

    return app.exec()
