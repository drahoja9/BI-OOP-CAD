import os

from PyQt5 import QtWidgets

from app.ui.main_window import Ui_MainWindow
from app.controller import Controller
from app.shapes_store import ShapesStore
from app.shapes import Rectangle, Dot, Line, Circle
from app.utils import Point


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # Here we choose, which printer we want to create and use
        controller = Controller()
        # If we choose CanvasPrinter, we must also add it to the canvasArea in the main window as a widget
        self._ui.scrollArea.setWidget(controller.canvas)

        self.show()
