from typing import Dict

import pytest

from app.shapes import Shape, Dot, Line, Rectangle, Circle, Polyline
from app.utils import Point, Color
from app.printers import Printer


class PrinterMockup(Printer):
    def __init__(self):
        super().__init__()
        self.result = ''

    def print_dot(self, dot: Dot):
        self.result = 'Drawed a ' + str(dot)

    def print_line(self, line: Line):
        self.result = 'Drawed a ' + str(line)

    def print_polyline(self, polyline: Polyline):
        self.result = 'Drawed a ' + str(polyline)

    def print_rectangle(self, rect: Rectangle):
        self.result = 'Drawed a ' + str(rect)

    def print_circle(self, circle: Circle):
        self.result = 'Drawed a ' + str(circle)


def test_abstract_shape():
    abstract_shape = Shape(Point(100, 100), Color(0, 1, 2))

    assert abstract_shape.start == Point(100, 100)
    assert abstract_shape.color == Color(0, 1, 2)

    with pytest.raises(NotImplementedError):
        abstract_shape.print_to(None)

    with pytest.raises(NotImplementedError):
        abstract_shape.get_props()

    with pytest.raises(NotImplementedError):
        abstract_shape.contains(Point(1, 1))

    assert str(abstract_shape) == ' with Color(0, 1, 2, alpha=255)'
    assert abstract_shape == Shape(Point(100, 100), Color(0, 1, 2))
    assert abstract_shape != Shape(Point(100, 101), Color(0, 1, 2))

    new_shape = abstract_shape.move(Point(100, 100), Point(-32, 123))
    assert abstract_shape.start == Point(100, 100)
    assert new_shape == Shape(Point(-32, 123), abstract_shape.color)


def test_dot(shapes: Dict[str, Shape]):
    dot = shapes['dot']

    assert dot.start == Point(10, 200000000)
    assert dot.color == Color(1, 2, 3)
    assert dot.get_props() == (10, 200000000)

    d = PrinterMockup()
    dot.print_to(d)
    assert d.result == 'Drawed a ' + str(dot)

    assert str(dot) == 'Dot at [10, 200000000] with Color(1, 2, 3, alpha=255)'
    assert dot == Dot(Point(10, 200000000), Color(1, 2, 3))
    assert dot != Dot(Point(10, 200000000), Color(1, 2, 4))
    assert dot.contains(Point(10, 200000000)) is True
    assert dot.contains(Point(11, 200000000), divergence=True) is True
    assert dot.contains(Point(11, 200000000)) is False
    assert dot.contains(Point(13, 200000000), divergence=True) is False

    new_dot = dot.move(Point(10, 200000000), Point(0, 0))
    assert dot.start == Point(10, 200000000)
    assert new_dot == Dot(Point(0, 0), dot.color)


def test_line(shapes: Dict[str, Shape]):
    line: Line = shapes['line']

    assert line.start == Point(1000, -1000)
    assert line.end == Point(0, -1000)
    assert line.color == Color(0, 0, 0)
    assert line.get_props() == (1000, -1000, 0, -1000)

    d = PrinterMockup()
    line.print_to(d)
    assert d.result == 'Drawed a ' + str(line)
    
    assert str(line) == 'Line from [1000, -1000] to [0, -1000] with Color(0, 0, 0, alpha=255)'
    assert line == Line(Point(1000, -1000), Point(0, -1000), Color(0, 0, 0))
    assert line != Line(Point(1000, -1000), Point(0, 1000), Color(0, 0, 0))
    assert line.contains(Point(500, -1000)) is True
    assert line.contains(Point(502, -1000), divergence=True) is True
    assert line.contains(Point(-1, -1000)) is False
    assert line.contains(Point(-3, -1000), divergence=False) is False

    # Vertical move
    new_line = line.move(Point(500, -1000), Point(500, 0))
    assert line.start == Point(1000, -1000)
    assert line.end == Point(0, -1000)
    assert new_line == Line(Point(1000, 0), Point(0, 0), line.color)

    # Horizontal move
    new_line = line.move(Point(1, -1000), Point(-999, -1000))
    assert line.start == Point(1000, -1000)
    assert line.end == Point(0, -1000)
    assert new_line == Line(Point(0, -1000), Point(-1000, -1000), line.color)

    # Diagonal move
    new_line = line.move(Point(350, -1000), Point(500, -1200))
    assert line.start == Point(1000, -1000)
    assert line.end == Point(0, -1000)
    assert new_line == Line(Point(1150, -1200), Point(150, -1200), line.color)


def test_polyline(shapes: Dict[str, Shape]):
    with pytest.raises(ValueError):
        Polyline(Point(10, 10), color=Color(0, 0, 0))

    polyline: Polyline = shapes['polyline']

    assert polyline.start == Point(10, 10)
    assert polyline.color == Color(48, 210, 111)
    assert polyline.get_props() == polyline.points == (Point(10, 10), Point(20, 20), Point(30, 10))

    d = PrinterMockup()
    polyline.print_to(d)
    assert d.result == 'Drawed a ' + str(polyline)
    
    assert str(polyline) == 'Polyline with points at ([10, 10], [20, 20], [30, 10]) with Color(48, 210, 111, alpha=255)'
    assert polyline == Polyline(Point(10, 10), Point(20, 20), Point(30, 10), color=Color(48, 210, 111))
    assert polyline != Polyline(Point(10, 10), Point(20, 20), color=Color(48, 210, 111))
    assert polyline.contains(Point(10, 10)) is True
    assert polyline.contains(Point(15, 15)) is True
    assert polyline.contains(Point(25, 15)) is True
    assert polyline.contains(Point(24.5, 15), divergence=True) is True
    assert polyline.contains(Point(15, 16)) is False
    assert polyline.contains(Point(24, 15)) is False
    assert polyline.contains(Point(24, 15), divergence=True) is False

    # Vertical move
    new_polyline = polyline.move(Point(20, 20), Point(20, 10))
    assert polyline.start == Point(10, 10)
    assert polyline.points[0] == Point(10, 10)
    assert polyline.points[1] == Point(20, 20)
    assert polyline.points[2] == Point(30, 10)
    assert new_polyline == Polyline(Point(10, 0), Point(20, 10), Point(30, 0), color=polyline.color)

    # Horizontal move
    new_polyline = polyline.move(Point(28, 12), Point(40, 12))
    assert polyline.start == Point(10, 10)
    assert polyline.points[0] == Point(10, 10)
    assert polyline.points[1] == Point(20, 20)
    assert polyline.points[2] == Point(30, 10)
    assert new_polyline == Polyline(Point(22, 10), Point(32, 20), Point(42, 10), color=polyline.color)

    # Diagonal move
    new_polyline = polyline.move(Point(15, 15), Point(10, 0))
    assert polyline.start == Point(10, 10)
    assert polyline.points[0] == Point(10, 10)
    assert polyline.points[1] == Point(20, 20)
    assert polyline.points[2] == Point(30, 10)
    assert new_polyline == Polyline(Point(5, -5), Point(15, 5), Point(25, -5), color=polyline.color)


def test_rectangle(shapes: Dict[str, Shape]):
    rect: Rectangle = shapes['rectangle']

    assert rect.start == Point(0, 0)
    assert rect.width == 1
    assert rect.height == 50000
    assert rect.color == Color(255, 255, 255)
    assert rect.get_props() == (0, 0, 1, 50000)

    d = PrinterMockup()
    rect.print_to(d)
    assert d.result == 'Drawed a ' + str(rect)
    
    assert str(rect) == '1x50000 rectangle with top-left corner at [0, 0] with Color(255, 255, 255, alpha=255)'
    assert rect == Rectangle(Point(0, 0), 1, 50000, Color(255, 255, 255))
    assert rect != Rectangle(Point(0, 0), -1, 50000, Color(255, 255, 255))
    assert rect.contains(Point(0, 0)) is True
    assert rect.contains(Point(1, 0)) is True
    assert rect.contains(Point(1, 50000)) is True
    assert rect.contains(Point(2, 0)) is False
    assert rect.contains(Point(0, 50001)) is False

    # Vertical move
    new_rect = rect.move(Point(1, 3500), Point(1, 0))
    assert rect.start == Point(0, 0)
    assert new_rect == Rectangle(Point(0, -3500), rect.width, rect.height, rect.color)

    # Horizontal move
    new_rect = rect.move(Point(0, 20), Point(20, 20))
    assert rect.start == Point(0, 0)
    assert new_rect == Rectangle(Point(20, 0), rect.width, rect.height, rect.color)

    # Diagonal move
    new_rect = rect.move(Point(1, 100), Point(20, 50))
    assert rect.start == Point(0, 0)
    assert new_rect == Rectangle(Point(19, -50), rect.width, rect.height, rect.color)


def test_circle(shapes: Dict[str, Shape]):
    circle: Circle = shapes['circle']

    assert circle.start == Point(12345, 54321)
    assert circle.radius == 999
    assert circle.color == Color(123, 255, 0)
    assert circle.get_props() == (12345, 54321, 999)

    d = PrinterMockup()
    circle.print_to(d)
    assert d.result == 'Drawed a ' + str(circle)
    
    assert str(circle) == 'Circle centered at [12345, 54321] with radius 999 with Color(123, 255, 0, alpha=255)'
    assert circle == Circle(Point(12345, 54321), 999, Color(123, 255, 0))
    assert circle != Circle(Point(12345, 54321), 999, Color(123, 255, 1))
    assert circle.contains(Point(12345, 54321)) is True
    assert circle.contains(Point(13344, 54321)) is True
    assert circle.contains(Point(12345, 53322)) is True
    assert circle.contains(Point(12344, 53322)) is False
    assert circle.contains(Point(13344, 54322)) is False

    # Vertical move
    new_circle = circle.move(Point(13344, 54321), Point(13344, 0))
    assert circle.start == Point(12345, 54321)
    assert new_circle == Circle(Point(12345, 0), circle.radius, circle.color)

    # Horizontal move
    new_circle = circle.move(Point(12345, 53322), Point(0, 53322))
    assert circle.start == Point(12345, 54321)
    assert new_circle == Circle(Point(0, 54321), circle.radius, circle.color)

    # Diagonal move
    new_circle = circle.move(Point(13344, 54321), Point(0, 0))
    assert circle.start == Point(12345, 54321)
    assert new_circle == Circle(Point(-999, 0), circle.radius, circle.color)


def test_shape_class_diff():
    abstract_shape = Shape(Point(100, 100), Color(100, 100, 100))
    dot = Dot(Point(100, 100), Color(100, 100, 100))
    line = Line(Point(100, 100), Point(100, 100), Color(100, 100, 100))
    polyline = Polyline(Point(100, 100), Point(100, 100), color=Color(100, 100, 100))
    rect = Rectangle(Point(100, 100), 100, 100, Color(100, 100, 100))
    circle = Circle(Point(100, 100), 100, Color(100, 100, 100))

    assert abstract_shape != dot != line != polyline != rect != circle
