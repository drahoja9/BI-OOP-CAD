from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QEvent

from app.shapes import Shape, Dot, Line, Rectangle, Circle


class Drawer:
    def __init__(self, shapes: list):
        super().__init__()
        if shapes is None:
            self._shapes = []
        else:
            self._shapes = shapes

    def add_shape(self, shape: Shape):
        self._shapes.append(shape)

    def add_shapes(self, *shapes: Shape):
        for shape in shapes:
            self.add_shape(shape)

    def draw_dot(self, dot: Dot):
        pass

    def draw_line(self, line: Line):
        pass

    def draw_rectangle(self, rect: Rectangle):
        pass

    def draw_circle(self, circle: Circle):
        pass


class Canvas(Drawer, QtWidgets.QWidget):
    def __init__(self, shapes: list = None):
        super().__init__(shapes)

    def _prepare_painter(self, color: QColor):
        painter = QPainter(self)
        painter.setBrush(color)
        return painter

    def paintEvent(self, event: QEvent):
        for obj in self._shapes:
            obj.draw(self)

    def draw_dot(self, dot: Dot):
        painter = self._prepare_painter(dot.color)
        painter.drawPoint(*dot.get_props())

    def draw_line(self, line: Line):
        painter = self._prepare_painter(line.color)
        painter.drawLine(*line.get_props())

    def draw_rectangle(self, rect: Rectangle):
        painter = self._prepare_painter(rect.color)
        painter.drawRect(*rect.get_props())

    def draw_circle(self, circle: Circle):
        painter = self._prepare_painter(circle.color)
        # There's no direct method for drawing circles in PyQt, so we have
        # to draw ellipse with radii rx and ry, where rx == ry
        painter.drawEllipse(*circle.get_props(), circle.radius)
