from typing import Dict

import pytest
from PyQt5.QtGui import QColor

from app.shapes import Shape, Dot, Line, Rectangle, Circle, Polyline
from app.utils import Point
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
    abstract_shape = Shape(Point(100, 100), QColor('steelblue'))

    assert abstract_shape.start == Point(100, 100)
    assert abstract_shape.color == QColor('steelblue')

    with pytest.raises(NotImplementedError):
        abstract_shape.print_to(None)

    with pytest.raises(NotImplementedError):
        abstract_shape.get_props()

    with pytest.raises(NotImplementedError):
        abstract_shape.contains(Point(1, 1))

    assert str(abstract_shape) == 'Abstract shape at [100, 100]'
    assert abstract_shape == Shape(Point(100, 100), QColor('steelblue'))
    assert abstract_shape != Shape(Point(100, 101), QColor('steelblue'))


def test_dot(shapes: Dict[str, Shape]):
    dot = shapes['dot']

    assert dot.start == Point(10, 200000000)
    assert dot.color == QColor(1, 2, 3)
    assert dot.get_props() == (10, 200000000)

    d = PrinterMockup()
    dot.print_to(d)
    assert d.result == 'Drawed a ' + str(dot)

    assert str(dot) == 'Dot at [10, 200000000]'
    assert dot == Dot(Point(10, 200000000), QColor(1, 2, 3))
    assert dot != Dot(Point(10, 200000000), QColor(1, 2, 4))
    assert dot.contains(Point(10, 200000000)) is True
    assert dot.contains(Point(11, 200000000)) is False


def test_line(shapes: Dict[str, Shape]):
    line: Line = shapes['line']

    assert line.start == Point(1000, -1000)
    assert line.end == Point(-123, 321)
    assert line.color == QColor(0, 0, 0)
    assert line.get_props() == (1000, -1000, -123, 321)

    d = PrinterMockup()
    line.print_to(d)
    assert d.result == 'Drawed a ' + str(line)

    assert str(line) == 'Line from [1000, -1000] to [-123, 321]'
    assert line == Line(Point(1000, -1000), Point(-123, 321), QColor(0, 0, 0))
    assert line != Line(Point(1000, -1000), Point(123, 321), QColor(0, 0, 0))
    assert line.contains(Point(1000, -1000)) is True
    assert line.contains(Point(1000, 1000)) is False


def test_polyline(shapes: Dict[str, Shape]):
    with pytest.raises(ValueError):
        Polyline(Point(10, 10), color=QColor(0, 0, 0))

    polyline: Polyline = shapes['polyline']

    assert polyline.start == Point(10, 10)
    assert polyline.color == QColor(48, 210, 111)
    assert polyline.get_props() == polyline.points == (Point(10, 10), Point(20, 20), Point(30, 10))

    d = PrinterMockup()
    polyline.print_to(d)
    assert d.result == 'Drawed a ' + str(polyline)

    assert str(polyline) == 'Polyline with points at ([10, 10], [20, 20], [30, 10])'
    assert polyline == Polyline(Point(10, 10), Point(20, 20), Point(30, 10), color=QColor(48, 210, 111))
    assert polyline != Polyline(Point(10, 10), Point(20, 20), color=QColor(48, 210, 111))
    assert polyline.contains(Point(10, 10)) is True
    assert polyline.contains(Point(15, 15)) is True
    assert polyline.contains(Point(25, 15)) is True
    assert polyline.contains(Point(15, 16)) is False
    assert polyline.contains(Point(24, 15)) is False


def test_rectangle(shapes: Dict[str, Shape]):
    rect: Rectangle = shapes['rectangle']

    assert rect.start == Point(0, 0)
    assert rect.width == 1
    assert rect.height == 50000
    assert rect.color == QColor(255, 255, 255)
    assert rect.get_props() == (0, 0, 1, 50000)

    d = PrinterMockup()
    rect.print_to(d)
    assert d.result == 'Drawed a ' + str(rect)

    assert str(rect) == '1x50000 rectangle with top-left corner at [0, 0]'
    assert rect == Rectangle(Point(0, 0), 1, 50000, QColor(255, 255, 255))
    assert rect != Rectangle(Point(0, 0), -1, 50000, QColor(255, 255, 255))
    assert rect.contains(Point(0, 0)) is True
    assert rect.contains(Point(1, 0)) is True
    assert rect.contains(Point(1, 50000)) is True
    assert rect.contains(Point(2, 0)) is False
    assert rect.contains(Point(0, 50001)) is False


def test_circle(shapes: Dict[str, Shape]):
    circle: Circle = shapes['circle']

    assert circle.start == Point(12345, 54321)
    assert circle.radius == 999
    assert circle.color == QColor(123, 255, 0)
    assert circle.get_props() == (12345, 54321, 999)

    d = PrinterMockup()
    circle.print_to(d)
    assert d.result == 'Drawed a ' + str(circle)

    assert str(circle) == 'Circle centered at [12345, 54321] with radius 999'
    assert circle == Circle(Point(12345, 54321), 999, QColor(123, 255, 0))
    assert circle != Circle(Point(12345, 54321), 999, QColor(123, 255, 1))
    assert circle.contains(Point(12345, 54321)) is True
    assert circle.contains(Point(13344, 54321)) is True
    assert circle.contains(Point(12345, 53322)) is True
    assert circle.contains(Point(12344, 53322)) is False
    assert circle.contains(Point(13344, 54322)) is False


def test_shape_class_diff():
    abstract_shape = Shape(Point(100, 100), QColor(100, 100, 100))
    dot = Dot(Point(100, 100), QColor(100, 100, 100))
    line = Line(Point(100, 100), Point(100, 100), QColor(100, 100, 100))
    polyline = Polyline(Point(100, 100), Point(100, 100), color=QColor(100, 100, 100))
    rect = Rectangle(Point(100, 100), 100, 100, QColor(100, 100, 100))
    circle = Circle(Point(100, 100), 100, QColor(100, 100, 100))

    assert abstract_shape != dot != line != polyline != rect != circle
