from typing import TextIO

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QPainter, QPen

from app.canvas import Canvas
from app.shapes import Dot, Line, Polyline, Rectangle, Circle, Shape
from app.utils import Color


class Printer:
    """
    Represents a visitor in the visitor design patter. Is responsible for HOW to print different shapes.
    """
    def update(self, controller):
        controller.print_all_shapes(self)

    def print_dot(self, dot: Dot):
        raise NotImplementedError

    def print_line(self, line: Line):
        raise NotImplementedError

    def print_polyline(self, polyline: Polyline):
        raise NotImplementedError

    def print_rectangle(self, rect: Rectangle):
        raise NotImplementedError

    def print_circle(self, circle: Circle):
        raise NotImplementedError


class AbstractTextPrinter(Printer):
    def __init__(self):
        super().__init__()

    def _print_shape(self, shape: Shape):
        raise NotImplementedError

    def print_dot(self, dot: Dot):
        self._print_shape(dot)

    def print_line(self, line: Line):
        self._print_shape(line)

    def print_polyline(self, polyline: Polyline):
        self._print_shape(polyline)

    def print_rectangle(self, rect: Rectangle):
        self._print_shape(rect)

    def print_circle(self, circle: Circle):
        self._print_shape(circle)


class StreamTextPrinter(AbstractTextPrinter):
    def __init__(self, stream: TextIO):
        super().__init__()
        self._stream = stream

    def _print_shape(self, shape: Shape):
        self._stream.write(str(shape) + '\n')


class FileTextPrinter(AbstractTextPrinter):
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._mode = 'a'

    def _print_shape(self, shape: Shape):
        with open(self._path, self._mode) as f:
            f.write(str(shape) + '\n')


class CanvasPrinter(Printer):
    def __init__(self, canvas: Canvas):
        super().__init__()
        self._canvas = canvas

    def update(self, controller):
        # Emitting the QEvent.Paint event to enable drawing
        self._canvas.update()

    def _prepare_painter(self, color: Color):
        painter = QPainter(self._canvas)
        # TODO: Do we want filled shapes or not???
        painter.setPen(QColor(*color))
        return painter

    def print_dot(self, dot: Dot):
        painter = self._prepare_painter(dot.color)
        pen = QPen(painter.brush(), 5)
        pen.setColor(QColor(*dot.color))
        painter.setPen(pen)
        painter.drawPoint(*dot.get_props())

    def print_line(self, line: Line):
        painter = self._prepare_painter(line.color)
        painter.drawLine(*line.get_props())

    def print_polyline(self, polyline: Polyline):
        painter = self._prepare_painter(polyline.color)
        q_points = []
        for point in polyline.get_props():
            q_points.append(QPointF(point.x, point.y))
        painter.drawPolyline(*q_points)

    def print_rectangle(self, rect: Rectangle):
        painter = self._prepare_painter(rect.color)
        painter.drawRect(*rect.get_props())

    def print_circle(self, circle: Circle):
        painter = self._prepare_painter(circle.color)
        # There's no direct method for drawing circles in PyQt, so we have
        # to draw ellipse outside a rectangle starting at [start_x, start_y],
        # with height and width set to radius of circle
        start_x = circle.start.x - circle.radius
        start_y = circle.start.y - circle.radius
        painter.drawEllipse(start_x, start_y, circle.radius * 2, circle.radius * 2)
