from typing import List

import pytest
from PyQt5.QtCore import Qt

from app.canvas import Canvas
from app.brushes import LineShapeBrush, RectShapeBrush, DotShapeBrush, CircleShapeBrush, MoveShapeBrush
from app.commands import Command, PrintDotCommand, PrintRectCommand
from app.gui import MainWindow
from app.shape_factory import PointsRectFactory
from app.shapes import Shape, Line, Rectangle
from app.utils import Point, Color


class ControllerMockup:
    def __init__(self):
        self.all_shapes = None
        self.command = None

    def print_all_shapes(self):
        self.all_shapes = 'printed all shapes'

    def execute_command(self, command: Command):
        self.command = command

    def end_preview(self):
        pass

    def shapes_at(self, point: Point) -> List[Shape]:
        return [Line(Point(0, 0), Point(0, 10), Color(10, 20, 30)), Rectangle(Point(0, 5), 10, 10, Color(0, 0, 0))]


class EventMockup:
    @staticmethod
    def x() -> int:
        return 10

    @staticmethod
    def y() -> int:
        return 20

    @staticmethod
    def buttons() -> Qt.LeftButton:
        return Qt.LeftButton


@pytest.fixture
def canvas(qtbot) -> Canvas:
    controller = ControllerMockup()

    gui = MainWindow(controller)
    gui.show()
    qtbot.addWidget(gui)

    canvas = Canvas(controller)
    assert canvas.hasMouseTracking() is True
    return canvas


def test_set_brush(canvas: Canvas):
    assert canvas.brush == MoveShapeBrush()
    assert canvas.cursor() == Qt.ArrowCursor

    canvas.set_brush(LineShapeBrush())
    assert canvas.brush.color == (255, 255, 255)
    assert canvas.brush == LineShapeBrush()
    assert canvas.cursor() == Qt.CrossCursor

    canvas.set_color((10, 20, 30))
    canvas.set_brush(RectShapeBrush())
    assert canvas.brush.color == (10, 20, 30)
    assert canvas.brush == RectShapeBrush()
    assert canvas.cursor() == Qt.CrossCursor

    canvas.set_brush()
    assert canvas.brush == MoveShapeBrush()
    assert canvas.cursor() == Qt.ArrowCursor


def test_set_color(canvas: Canvas):
    assert canvas.color == (255, 255, 255)

    canvas.set_brush(CircleShapeBrush())
    canvas.set_color((100, 200, 100))
    assert canvas.color == (100, 200, 100)
    assert canvas.brush.color == (100, 200, 100)


def test_pain_event(canvas: Canvas):
    canvas.paintEvent(EventMockup)
    assert canvas._controller.all_shapes == 'printed all shapes'


def test_mouse_move_event(canvas: Canvas):
    assert canvas.brush == MoveShapeBrush()
    assert canvas.cursor() == Qt.ArrowCursor

    canvas.mouseMoveEvent(EventMockup)
    assert (
        canvas._controller.command
        is None
    )

    canvas.set_brush(DotShapeBrush())
    canvas.mouseMoveEvent(EventMockup)
    assert (
        canvas._controller.command
        ==
        PrintDotCommand(canvas._controller, EventMockup.x(), EventMockup.y(), (255, 255, 255))
    )
    assert canvas.cursor() == Qt.CrossCursor


def test_mouse_press_event(canvas: Canvas):
    assert canvas.brush == MoveShapeBrush()
    assert canvas.cursor() == Qt.ArrowCursor

    canvas.mousePressEvent(EventMockup)
    assert canvas._controller.command is None

    canvas.set_brush(RectShapeBrush())
    canvas.mousePressEvent(EventMockup)
    canvas.mousePressEvent(EventMockup)
    assert (
        canvas._controller.command
        ==
        PrintRectCommand(
            receiver=canvas._controller,
            start_x=EventMockup.x(), start_y=EventMockup.y(),
            color=(255, 255, 255),
            rect_factory=PointsRectFactory,
            end_x=EventMockup.x(), end_y=EventMockup.y()
        )
    )
