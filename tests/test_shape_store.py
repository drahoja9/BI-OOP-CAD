from typing import Dict

import pytest
from PyQt5.QtGui import QColor

from app.shapes import Circle, Rectangle, Line, Dot, Polyline
from app.printers import Printer
from app.shapes_store import ShapesStore
from app.shapes import Shape
from app.utils import Point


class ControllerMockup:
    def __init__(self):
        self.result = []

    def update_canvas(self):
        self.result.append('canvas updated')


class PrinterMockup(Printer):
    def __init__(self):
        super().__init__()
        self.dot = ''
        self.line = ''
        self.polyline = ''
        self.rect = ''
        self.circle = ''

    def print_dot(self, dot: Dot):
        self.dot += 'printed'

    def print_line(self, line: Line):
        self.line += 'printed'

    def print_polyline(self, polyline: Polyline):
        self.polyline += 'printed'

    def print_rectangle(self, rect: Rectangle):
        self.rect += 'printed'

    def print_circle(self, circle: Circle):
        self.circle += 'printed'


@pytest.fixture
def shapes_store() -> ShapesStore:
    controller = ControllerMockup()
    shapes_store = ShapesStore(controller)
    return shapes_store


def test_is_empty(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    assert shapes_store.is_empty() is True

    shapes_store.add_shapes(shapes['circle'])
    assert shapes_store.is_empty() is False


def test_print_all(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    shapes_store.add_shapes(*shapes.values())
    shapes_store.set_preview(shapes['rectangle'])
    printer = PrinterMockup()
    shapes_store.print_all(printer)

    assert printer.dot == 'printed'
    assert printer.line == 'printed'
    assert printer.rect == 'printedprinted'
    assert printer.circle == 'printed'


def test_set_preview(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    assert shapes_store._preview is None
    shapes_store.set_preview(shapes['line'])
    assert shapes_store._preview == shapes['line']
    assert len(shapes_store._controller.result) == 1


def test_add_shapes(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    shapes_store.add_shapes(shapes['dot'])
    assert shapes_store._shapes.index(shapes['dot']) == 0
    assert len(shapes_store._controller.result) == 1
    assert len(shapes_store._shapes) == 1

    shapes_store.add_shapes(shapes['line'], shapes['rectangle'], shapes['circle'])
    assert shapes_store._shapes.index(shapes['line']) == 1
    assert shapes_store._shapes.index(shapes['rectangle']) == 2
    assert shapes_store._shapes.index(shapes['circle']) == 3
    assert len(shapes_store._controller.result) == 2
    assert len(shapes_store._shapes) == 4


def test_remove_last_shape(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    # Removing last shape if there are no shapes at all shouldn't do anything
    shapes_store.remove_last_shape()

    shapes_store.add_shapes(*shapes.values())
    shapes_store.remove_last_shape()
    last_item = shapes['circle']

    assert len(shapes_store._controller.result) == 2
    assert len(shapes_store._shapes) == len(shapes) - 1
    assert last_item not in shapes_store._shapes


def test_remove_shapes_at(shapes_store: ShapesStore):
    r1 = Rectangle(Point(0, 0), 100, 100, QColor(0, 0, 0))
    r2 = Rectangle(Point(1, 1), 100, 100, QColor(0, 0, 0))
    c = Circle(Point(0, 0), 50, QColor(0, 0, 0))
    l1 = Line(Point(-10, 0), Point(10, 0), QColor(0, 0, 0))
    l2 = Line(Point(-10, 1), Point(10, 1), QColor(0, 0, 0))
    d = Dot(Point(0, 0), QColor(0, 0, 0))

    shapes_store.add_shapes(r1, r2, c, l1, l2, d)
    removed = shapes_store.remove_shapes_at(Point(0, 0))

    assert removed == [r1, c, l1, d]
    assert shapes_store._shapes == [r2, l2]


def test_restart(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    shapes_store.add_shapes(*shapes.values())
    shapes_store._preview = shapes['line']
    shapes_store.restart()

    assert shapes_store.is_empty() is True
    assert shapes_store._preview is None
    assert len(shapes_store._controller.result) == 2
