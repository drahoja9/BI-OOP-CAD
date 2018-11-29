from typing import TextIO

from PyQt5.QtGui import QColor, QPainter

from app.canvas import Canvas
from app.shapes import Dot, Line, Rectangle, Circle


class Printer:
    """
    Represents a visitor in the visitor design patter. Is responsible for HOW to print different shapes.
    """
    def print_dot(self, dot: Dot):
        raise NotImplementedError

    def print_line(self, line: Line):
        raise NotImplementedError

    def print_rectangle(self, rect: Rectangle):
        raise NotImplementedError

    def print_circle(self, circle: Circle):
        raise NotImplementedError


class TextPrinter(Printer):
    def __init__(self, stream: TextIO):
        super().__init__()
        self._stream = stream

    def print_dot(self, dot: Dot):
        self._stream.write(str(dot) + '\n')

    def print_line(self, line: Line):
        self._stream.write(str(line) + '\n')

    def print_rectangle(self, rect: Rectangle):
        self._stream.write(str(rect) + '\n')

    def print_circle(self, circle: Circle):
        self._stream.write(str(circle) + '\n')


class FilePrinter(TextPrinter):
    def __init__(self, path: str, append: bool = True):
        mode = 'a' if append else 'w'
        self._fd = open(path, mode)
        super().__init__(self._fd)

    def __del__(self):
        self._fd.close()


class CanvasPrinter(Printer):
    def __init__(self, canvas: Canvas):
        super().__init__()
        self._canvas = canvas

    def _prepare_painter(self, color: QColor):
        painter = QPainter(self._canvas)
        painter.setBrush(color)
        return painter

    def print_dot(self, dot: Dot):
        painter = self._prepare_painter(dot.color)
        painter.drawPoint(*dot.get_props())

    def print_line(self, line: Line):
        painter = self._prepare_painter(line.color)
        painter.drawLine(*line.get_props())

    def print_rectangle(self, rect: Rectangle):
        painter = self._prepare_painter(rect.color)
        painter.drawRect(*rect.get_props())

    def print_circle(self, circle: Circle):
        painter = self._prepare_painter(circle.color)
        # There's no direct method for drawing circles in PyQt, so we have
        # to draw ellipse with radii rx and ry, where rx == ry
        painter.drawEllipse(*circle.get_props(), circle.radius)
