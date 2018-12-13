from typing import Dict

import pytest

from app.shapes import Circle, Rectangle, Line, Dot, Polyline
from app.printers import Printer
from app.shapes_store import ShapesStore
from app.shapes import Shape


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

    shapes_store.add_shape(shapes['circle'])
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


def test_add_shape(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    shapes_store.add_shape(shapes['dot'])
    assert shapes_store._shapes.index(shapes['dot']) == 0
    assert len(shapes_store._controller.result) == 1
    assert len(shapes_store._shapes) == 1


def test_add_shapes(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    shapes_store.add_shapes(*shapes.values())

    assert len(shapes_store._controller.result) == len(shapes)
    assert len(shapes_store._shapes) == len(shapes)

    for idx, shape in enumerate(shapes_store._shapes):
        key = [*shapes][idx]
        assert shape == shapes[key]


def test_remove_last_shape(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    # Removing last shape if there are no shapes at all shouldn't do anything
    shapes_store.remove_last_shape()

    shapes_store.add_shapes(*shapes.values())
    shapes_store.remove_last_shape()
    last_item = shapes[[*shapes][len(shapes)-1]]

    assert len(shapes_store._controller.result) == len(shapes) + 1
    assert len(shapes_store._shapes) == len(shapes) - 1
    assert last_item not in shapes_store._shapes


def test_remove_shape(shapes_store: ShapesStore, shapes: Dict[str, Shape]):
    shapes_store.add_shapes(*shapes.values())
    for shape in shapes.values():
        shapes_store.remove_shape(shape)
        assert shape not in shapes_store._shapes

    assert len(shapes_store._controller.result) == 2 * len(shapes)
    assert len(shapes_store._shapes) == 0

    # Removing shape that's not inside shouldn't do anything
    shapes_store.remove_shape(shapes['line'])
