import math
from typing import List, Tuple

from app.shapes import Dot, Line, Rectangle, Circle, Polyline
from app.utils import Point, Color


class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def __str__(self):
        return 'Abstract command, should not be instantiated!'

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.receiver == other.receiver


class ShapeCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)
        self.shape = None

    def execute(self):
        self.receiver.add_shape(self.shape)

    def reverse(self):
        self.receiver.remove_shape(self.shape)

    def __eq__(self, other):
        return super().__eq__(other) and self.shape == other.shape


class PrintDotCommand(ShapeCommand):
    def __init__(self, receiver, x: int, y: int, color: tuple):
        super().__init__(receiver)
        self.shape = Dot(
            Point(x, y),
            Color(*color)
        )

    def __str__(self):
        return f'dot {self.shape.start.x},{self.shape.start.y}'


class PrintLineCommand(ShapeCommand):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: tuple):
        super().__init__(receiver)
        self.shape = Line(
            Point(start_x, start_y),
            Point(end_x, end_y),
            Color(*color)
        )

    def __str__(self):
        return f'line {self.shape.start.x},{self.shape.start.y} {self.shape.end.x},{self.shape.end.y}'


class PrintPolylineCommand(ShapeCommand):
    def __init__(self, receiver, points: List[Tuple[int, int]], color: tuple):
        super().__init__(receiver)
        points_ = []
        for point in points:
            points_.append(Point(point[0], point[1]))
        self.shape = Polyline(*points_, color=Color(*color))

    def __str__(self):
        res = f'line'
        for point in self.shape.get_props():
            res += f' {point.x},{point.y}'
        return res


class PrintRectCommand(ShapeCommand):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: tuple):
        super().__init__(receiver)
        width = abs(start_x - end_x)
        height = abs(start_y - end_y)
        self.shape = Rectangle(
            Point(min(start_x, end_x), min(start_y, end_y)),
            width,
            height,
            Color(*color)
        )

    def __str__(self):
        return f'rect {self.shape.start.x},{self.shape.start.y} {self.shape.width} {self.shape.height}'


class PrintCircleCommand(ShapeCommand):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: tuple):
        super().__init__(receiver)
        center = (start_x, start_y)
        # Classic formula for distance of two points
        radius = math.floor(
            math.sqrt((start_x - end_x) ** 2 + (start_y - end_y) ** 2)
        )
        self.shape = Circle(
            Point(*center),
            radius,
            Color(*color)
        )

    def __str__(self):
        return f'circle {self.shape.start.x},{self.shape.start.y} {self.shape.radius}'
