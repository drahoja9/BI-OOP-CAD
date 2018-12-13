import copy
from typing import Type

import pytest
from PyQt5.QtCore import Qt

from app.brushes import Brush, DotBrush, LineBrush, RectBrush, CircleBrush, PolylineBrush
from app.commands import PrintDotCommand, PrintLineCommand, PrintRectCommand, PrintCircleCommand, Command, ShapeCommand, \
    PrintPolylineCommand
from app.shapes import Shape


class ControllerMockup:
    def __init__(self):
        self.command = None
        self.preview = None

    def execute_command(self, command: Command):
        self.command = command

    def preview_shape(self, shape: Shape):
        self.preview = shape

    def end_preview(self):
        self.preview = None


@pytest.fixture
def controller() -> ControllerMockup:
    return ControllerMockup()


def test_abstract_brush():
    b1 = Brush()
    b2 = Brush()
    assert b1 == b2

    with pytest.raises(AttributeError):
        b1.mouse_move(None, 1, 2, None)

    with pytest.raises(AttributeError):
        b1.mouse_press(None, 1, 2, None)


def test_dot_brush(controller: ControllerMockup):
    b1 = DotBrush()
    b2 = DotBrush()
    assert b1 == b2

    b1.mouse_move(controller, 10, 20, Qt.LeftButton)
    assert controller.command == PrintDotCommand(controller, 10, 20, (0, 0, 0))

    b1.mouse_press(controller, 123, 321, Qt.LeftButton)
    assert controller.command == PrintDotCommand(controller, 123, 321, (0, 0, 0))


def test_polyline_brush(controller: ControllerMockup):
    b1 = PolylineBrush()
    b2 = PolylineBrush()
    assert b1 == b2

    b1.mouse_move(controller, 10, 20, None)
    assert controller.command is None
    assert controller.preview is None

    points = []
    for x in range(0, 1000, 100):
        points.append((x, x))
        shape_command = PrintPolylineCommand(controller, [*points, (x*x, x+x)], (255, 255, 255))
        preview_shape = copy.deepcopy(shape_command.shape)
        preview_shape.color.setAlpha(200)

        b1.mouse_press(controller, x, x, Qt.LeftButton)
        b1.mouse_move(controller, x*x, x+x, None)
        assert controller.command is None
        assert controller.preview == preview_shape

    b1.mouse_press(controller, -999, 100, Qt.RightButton)
    assert controller.command == PrintPolylineCommand(controller, [*points, (-999, 100)], (255, 255, 255))
    assert controller.preview is None


@pytest.mark.parametrize('brush_class, shape_command_class', [
    (LineBrush, PrintLineCommand),
    (RectBrush, PrintRectCommand),
    (CircleBrush, PrintCircleCommand)
])
def test_brush(controller: ControllerMockup, brush_class: Type[Brush], shape_command_class: Type[ShapeCommand]):
    b1 = brush_class()
    b2 = brush_class()
    assert b1 == b2
    assert b1._shape_command_class == b2._shape_command_class == shape_command_class

    shape_command = shape_command_class(controller, -999, 0, -999, 100, (255, 255, 255))
    preview_shape = copy.deepcopy(shape_command.shape)
    preview_shape.color.setAlpha(200)

    b1.mouse_move(controller, 10, 20, None)
    assert controller.command is None
    assert controller.preview is None

    b1.mouse_press(controller, -999, 0, Qt.LeftButton)
    b1.mouse_move(controller, -999, 100, None)
    assert controller.command is None
    assert controller.preview == preview_shape

    b1.mouse_press(controller, -999, 100, Qt.LeftButton)
    assert controller.command == shape_command
    assert controller.preview is None