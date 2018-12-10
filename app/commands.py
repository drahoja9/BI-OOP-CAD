import math
from typing import Tuple

from PyQt5.QtGui import QColor

from app.shapes import Dot, Line, Rectangle, Circle
from app.utils import Point


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


class PrintDotCommand(Command):
    def __init__(self, receiver, x: int, y: int, color: Tuple[int, int, int]):
        super().__init__(receiver)
        self.dot = Dot(
            Point(x, y),
            QColor(*color)
        )

    def execute(self):
        self.receiver.add_shape(self.dot)

    def reverse(self) -> Command:
        pass

    def __str__(self):
        return (
            'dot ' +
            str(self.dot.start.x) +
            ',' +
            str(self.dot.start.y)
        )

    def __eq__(self, other):
        return super().__eq__(other) and self.dot == other.dot


class PrintLineCommand(Command):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: Tuple[int, int, int]):
        super().__init__(receiver)
        self.line = Line(
            Point(start_x, start_y),
            Point(end_x, end_y),
            QColor(*color)
        )

    def execute(self):
        self.receiver.add_shape(self.line)

    def reverse(self):
        pass

    def __str__(self):
        return (
            'line ' +
            str(self.line.start.x) +
            ',' +
            str(self.line.start.y) +
            ' ' +
            str(self.line.end.x) +
            ',' +
            str(self.line.end.y)
        )

    def __eq__(self, other):
        return super().__eq__(other) and self.line == other.line


# class PrintPolylineCommand(Command):
#     def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: Tuple[int, int, int]):
#         super().__init__(receiver)
#         self._line = Line(Point(start_x, start_y), Point(end_x, end_y), QColor(*color))
#
#     def execute(self):
#         self._receiver.add_shape(self._line)
#
#     def reverse(self):
#         pass


class PrintRectCommand(Command):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: Tuple[int, int, int]):
        super().__init__(receiver)
        width = abs(start_x - end_x)
        height = abs(start_y - end_y)
        self.rect = Rectangle(
            Point(min(start_x, end_x), min(start_y, end_y)),
            width,
            height,
            QColor(*color)
        )

    def execute(self):
        self.receiver.add_shape(self.rect)

    def reverse(self) -> Command:
        pass

    def __str__(self):
        return (
            'rect ' +
            str(self.rect.start.x) +
            ',' +
            str(self.rect.start.y) +
            ' ' +
            str(self.rect.width) +
            ' ' +
            str(self.rect.height)
        )

    def __eq__(self, other):
        return super().__eq__(other) and self.rect == other.rect


class PrintCircleCommand(Command):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: Tuple[int, int, int]):
        super().__init__(receiver)
        center = (start_x, start_y)
        # Classic formula for distance of two points
        radius = math.floor(
            math.sqrt((start_x - end_x) ** 2 + (start_y - end_y) ** 2)
        )
        self.circle = Circle(
            Point(*center),
            radius,
            QColor(*color)
        )

    def execute(self):
        self.receiver.add_shape(self.circle)

    def reverse(self) -> Command:
        pass

    def __str__(self):
        return (
            'circle ' +
            str(self.circle.start.x) +
            ',' +
            str(self.circle.start.y) +
            ' ' +
            str(self.circle.radius)
        )

    def __eq__(self, other):
        return super().__eq__(other) and self.circle == other.circle
