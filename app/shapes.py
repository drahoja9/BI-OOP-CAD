from PyQt5.QtGui import QColor

from app.utils import Point


class Shape:
    def __init__(self, start: Point, color: QColor):
        self.start = start
        self.color = color

    def draw(self, drawer):
        pass

    def get_props(self):
        pass


class Dot(Shape):
    def __init__(self, start: Point, color: QColor):
        super().__init__(start, color)

    def draw(self, drawer):
        drawer.draw_dot(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y


class Line(Shape):
    def __init__(self, start: Point, end: Point, color: QColor):
        super().__init__(start, color)
        self.end = end

    def draw(self, drawer):
        drawer.draw_line(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.end.x, self.end.y


class Rectangle(Shape):
    def __init__(self, top_left: Point, width: int, height: int, color: QColor):
        super().__init__(top_left, color)
        self.width = width
        self.height = height

    def draw(self, drawer):
        drawer.draw_rectangle(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.width, self.height


class Circle(Shape):
    def __init__(self, middle: Point, radius: int, color: QColor):
        super().__init__(middle, color)
        self.radius = radius

    def draw(self, drawer):
        drawer.draw_circle(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.radius
