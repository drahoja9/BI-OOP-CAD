from PyQt5.QtGui import QColor

from app.utils import Point


class Shape:
    def __init__(self, start: Point, color: QColor):
        self.start = start
        self.color = color

    def draw(self, drawer):
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

    def draw(self, drawer):
        drawer.draw_dot(self)

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

    def draw(self, drawer):
        drawer.draw_line(self)

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


class Rectangle(Shape):
    def __init__(self, top_left: Point, width: int, height: int, color: QColor):
        super().__init__(top_left, color)
        self.width = width
        self.height = height

    def draw(self, drawer):
        drawer.draw_rectangle(self)

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
    def __init__(self, middle: Point, radius: int, color: QColor):
        super().__init__(middle, color)
        self.radius = radius

    def draw(self, drawer):
        drawer.draw_circle(self)

    def get_props(self) -> tuple:
        return self.start.x, self.start.y, self.radius

    def __repr__(self):
        return (
            'Circle centered at ' +
            str(self.start) +
            ' with radius ' +
            str(self.radius)
        )

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.radius == other.radius
        )
