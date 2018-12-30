import math
from typing import Tuple

from app.utils import Point, distance, Color


class Shape:
    """
    Represents an object that is visited by a visitor in the visitor design pattern.
    """

    def __init__(self, start: Point, color: Color = Color(0, 0, 0)):
        self.start = start
        self.color = color

    def print_to(self, printer):
        raise NotImplementedError

    def get_props(self):
        raise NotImplementedError

    def contains(self, point: Point) -> bool:
        raise NotImplementedError

    def __repr__(self):
        return f' with {self.color}'

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.start == other.start and
            self.color == other.color
        )

    def __ne__(self, other):
        return not self.__eq__(other)


class Dot(Shape):
    def __init__(self, start: Point, color: Color):
        super().__init__(start, color)

    def print_to(self, printer):
        printer.print_dot(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y

    def contains(self, point: Point) -> bool:
        return self.start == point

    def __repr__(self):
        return f'Dot at {self.start}' + super().__repr__()


class Line(Shape):
    def __init__(self, start: Point, end: Point, color: Color):
        super().__init__(start, color)
        self.end = end

    def print_to(self, printer):
        printer.print_line(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.end.x, self.end.y

    def contains(self, point: Point) -> bool:
        return math.isclose(
            distance(self.start, point) + distance(self.end, point),
            distance(self.start, self.end)
        )

    def __repr__(self):
        return f'Line from {self.start} to {self.end}' + super().__repr__()

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.end == other.end
        )


class Polyline(Shape):
    def __init__(self, *points: Point, color: Color):
        if len(points) < 2:
            raise ValueError('There must be at least 2 points to define a Polyline!')
        super().__init__(points[0], color)
        self.points = points

    def print_to(self, printer):
        printer.print_polyline(self)

    def get_props(self) -> Tuple[Point]:
        return self.points

    def contains(self, point: Point) -> bool:
        for i in range(len(self.points) - 1):
            if math.isclose(
                distance(self.points[i], point) + distance(self.points[i + 1], point),
                distance(self.points[i], self.points[i + 1])
            ):
                return True
        return False

    def __repr__(self):
        return f'Polyline with points at {self.points}' + super().__repr__()

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.points == other.points
        )


class Rectangle(Shape):
    def __init__(self, top_left: Point, width: int, height: int, color: Color):
        super().__init__(top_left, color)
        self.width = width
        self.height = height

    def print_to(self, printer):
        printer.print_rectangle(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.width, self.height

    def contains(self, point: Point) -> bool:
        return (
            self.start.x <= point.x <= self.start.x + self.width
            and
            self.start.y <= point.y <= self.start.y + self.height
        )

    def __repr__(self):
        return f'{self.width}x{self.height} rectangle with top-left corner at {self.start}' + super().__repr__()

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.width == other.width and
            self.height == other.height
        )


class Circle(Shape):
    def __init__(self, center: Point, radius: int, color: Color):
        super().__init__(center, color)
        self.radius = radius

    def print_to(self, printer):
        printer.print_circle(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.radius

    def contains(self, point: Point) -> bool:
        return distance(self.start, point) <= self.radius

    def __repr__(self):
        return f'Circle centered at {self.start} with radius {self.radius}' + super().__repr__()

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.radius == other.radius
        )
