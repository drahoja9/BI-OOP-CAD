from PyQt5.QtGui import QColor

from app.gui import MainWindow
from app.commands import CommandEngine
from app.printers import CanvasPrinter
from app.shapes import Rectangle, Point, Dot, Line, Circle
from app.shapes_store import ShapesStore


class Controller:
    """
    Main class of this application. Holds all crucial pieces together.
    It represents a subject in the observer design pattern.
    """
    def __init__(self):
        self._gui = MainWindow(self)
        self._command_engine = CommandEngine()
        self._shapes = ShapesStore(self)
        self._printer = CanvasPrinter(self._gui.canvas)

        r1 = Rectangle(Point(10, 10), 200, 100, QColor(200, 0, 0))
        r2 = Rectangle(Point(100, 100), 20, 10, QColor(0, 200, 0))
        r3 = Rectangle(Point(400, 100), 50, 250, QColor(0, 0, 200))

        dot = Dot(Point(400, 400), QColor(10, 10, 10))

        line = Line(Point(0, 0), Point(953, 551), QColor(0, 0, 250))

        circle = Circle(Point(700, 50), 300, QColor(0, 250, 0))

        self._shapes.add_shapes(r1, r2, r3, dot, line, circle)
        # Run the whole app
        self._gui.run()

    def print_all_shapes(self):
        self._shapes.print_all(self._printer)

    def update_canvas(self):
        self._gui.canvas.update()
