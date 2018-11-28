import pytest

from PyQt5.QtGui import QColor

from app.shapes import Shape, Dot, Line, Rectangle, Circle
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

    assert str(abstract_shape) == 'Abstract shape at [100, 100]'
    assert abstract_shape == Shape(Point(100, 100), QColor('steelblue'))
    assert abstract_shape != Shape(Point(100, 101), QColor('steelblue'))


def test_dot():
    dot = Dot(Point(10, 200000000), QColor(1, 2, 3))

    assert dot.start == Point(10, 200000000)
    assert dot.color == QColor(1, 2, 3)
    assert dot.get_props() == (10, 200000000)

    d = PrinterMockup()
    dot.print_to(d)
    assert d.result == 'Drawed a ' + str(dot)

    assert str(dot) == 'Dot at [10, 200000000]'
    assert dot == Dot(Point(10, 200000000), QColor(1, 2, 3))
    assert dot != Dot(Point(10, 200000000), QColor(1, 2, 4))


def test_line():
    line = Line(Point(1000, -1000), Point(-123, 321), QColor(0, 0, 0))

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


def test_rectangle():
    rect = Rectangle(Point(0, 0), 1, 50000, QColor(255, 255, 255))

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


def test_circle():
    circle = Circle(Point(12345, 54321), 999, QColor(123, 255, 0))

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


def test_equals():
    abstract_shape = Shape(Point(100, 100), QColor(100, 100, 100))
    dot = Dot(Point(100, 100), QColor(100, 100, 100))
    line = Line(Point(100, 100), Point(100, 100), QColor(100, 100, 100))
    rect = Rectangle(Point(100, 100), 100, 100, QColor(100, 100, 100))
    circle = Circle(Point(100, 100), 100, QColor(100, 100, 100))

    assert abstract_shape != dot != line != rect != circle
