from typing import List

from PyQt5.QtGui import QColor

from app.utils import Point


class Shape:
    """
    Represents an object that is visited by a visitor in the visitor design pattern.
    """

    def __init__(self, start: Point, color: QColor = None):
        self.start = start
        self.color = color

    def print_to(self, printer):
        raise NotImplementedError

    def get_props(self):
        raise NotImplementedError

    def __repr__(self):
        return (
            'Abstract shape at ' +
            str(self.start)
        )

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.start == other.start and
            self.color == other.color
        )

    def __ne__(self, other):
        return not self.__eq__(other)


class Dot(Shape):
    def __init__(self, start: Point, color: QColor):
        super().__init__(start, color)

    def print_to(self, printer):
        printer.print_dot(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y

    def __repr__(self):
        return (
            'Dot at ' +
            str(self.start)
        )


class Line(Shape):
    def __init__(self, start: Point, end: Point, color: QColor):
        super().__init__(start, color)
        self.end = end

    def print_to(self, printer):
        printer.print_line(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.end.x, self.end.y

    def __repr__(self):
        return (
            'Line from ' +
            str(self.start) +
            ' to ' +
            str(self.end)
        )

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.end == other.end
        )


# class Polyline(Shape):
#     def __init__(self, lines: List[Line]):
#         super().__init__(lines[0].start)
#         self.lines = lines
#
#     def print_to(self, printer):
#         printer.print_polyline(self)
#
#     def get_props(self):
#         pass
#
#     def __repr__(self):
#         return (
#             'Polyline composed of [' +
#             str(self.lines) +
#             ']'
#         )
#
#     def __eq__(self, other):
#         return (
#             super().__eq__(other) and
#             self.lines == other.lines
#         )


class Rectangle(Shape):
    def __init__(self, top_left: Point, width: int, height: int, color: QColor):
        super().__init__(top_left, color)
        self.width = width
        self.height = height

    def print_to(self, printer):
        printer.print_rectangle(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.width, self.height

    def __repr__(self):
        return (
            str(self.width) +
            'x' +
            str(self.height) +
            ' rectangle with top-left corner at ' +
            str(self.start)
        )

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.width == other.width and
            self.height == other.height
        )


class Circle(Shape):
    def __init__(self, middle: Point, diameter: int, color: QColor):
        super().__init__(middle, color)
        self.diameter = diameter

    def print_to(self, printer):
        printer.print_circle(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.diameter

    def __repr__(self):
        return (
            'Circle centered at ' +
            str(self.start) +
            ' with diameter ' +
            str(self.diameter)
        )

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.diameter == other.diameter
        )
