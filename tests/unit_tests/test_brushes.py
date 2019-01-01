import copy
from typing import Type, List

import pytest
from PyQt5.QtCore import Qt

from app.brushes import ShapeBrush, DotShapeBrush, LineShapeBrush, RectShapeBrush, CircleShapeBrush, PolylineShapeBrush, \
    Brush, RemoveShapeBrush, MoveShapeBrush
from app.commands import PrintDotCommand, PrintLineCommand, PrintRectCommand, PrintCircleCommand, Command, ShapeCommand, \
    PrintPolylineCommand, RemoveShapeCommand, MoveShapeCommand
from app.shapes import Shape, Line, Rectangle
from app.utils import Color, Point


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

    def shapes_at(self, point: Point) -> List[Shape]:
        shapes = [Line(Point(0, 0), Point(0, 10), Color(10, 20, 30)), Rectangle(Point(0, 5), 10, 10, Color(0, 0, 0))]
        return [shape for shape in shapes if shape.contains(point)]


@pytest.fixture
def controller() -> ControllerMockup:
    return ControllerMockup()


def test_abstract_brush():
    b = Brush()

    with pytest.raises(NotImplementedError):
        b.mouse_move(None, 1, 2, None)

    with pytest.raises(NotImplementedError):
        b.mouse_press(None, 1, 2, None)


def test_abstract_shape_brush():
    b1 = ShapeBrush()
    b2 = ShapeBrush()
    assert b1 == b2

    with pytest.raises(AttributeError):
        b1.mouse_move(None, 1, 2, None)

    with pytest.raises(AttributeError):
        b1.mouse_press(None, 1, 2, None)


def test_dot_brush(controller: ControllerMockup):
    b1 = DotShapeBrush()
    b2 = DotShapeBrush()
    assert b1 == b2
    assert str(b1) == str(b2) == 'Dot'

    b1.mouse_move(controller, 10, 20, Qt.LeftButton)
    assert controller.command == PrintDotCommand(receiver=controller, x=10, y=20, color=(0, 0, 0))

    b1.mouse_press(controller, 123, 321, Qt.LeftButton)
    assert controller.command == PrintDotCommand(receiver=controller, x=123, y=321, color=(0, 0, 0))


def test_polyline_brush(controller: ControllerMockup):
    b1 = PolylineShapeBrush()
    b2 = PolylineShapeBrush()
    assert b1 == b2
    assert str(b1) == str(b2) == 'Polyline'

    b1.mouse_move(controller, 10, 20, None)
    assert controller.command is None
    assert controller.preview is None

    points = []
    for x in range(0, 1000, 100):
        points.append((x, x))
        shape_command = PrintPolylineCommand(
            receiver=controller,
            points=[*points, (x * x, x + x)],
            color=(0, 0, 0, 200)
        )
        preview_shape = copy.deepcopy(shape_command.shape)

        b1.mouse_press(controller, x, x, Qt.LeftButton)
        b1.mouse_move(controller, x * x, x + x, None)
        assert controller.command is None
        assert controller.preview == preview_shape

    b1.mouse_press(controller, -999, 100, Qt.RightButton)
    assert controller.command == PrintPolylineCommand(
        receiver=controller,
        points=[*points, (-999, 100)],
        color=(0, 0, 0)
    )
    assert controller.preview is None
    assert b1._points == []


@pytest.mark.parametrize('brush_class, shape_command_class, shape_name', [
    (LineShapeBrush, PrintLineCommand, 'Line'),
    (RectShapeBrush, PrintRectCommand, 'Rectangle'),
    (CircleShapeBrush, PrintCircleCommand, 'Circle')
])
def test_shape_brush(
    controller: ControllerMockup,
    brush_class: Type[ShapeBrush],
    shape_command_class: Type[ShapeCommand],
    shape_name: str
):
    b1 = brush_class()
    b2 = brush_class()
    assert b1 == b2
    assert b1._shape_command_class == b2._shape_command_class == shape_command_class
    assert str(b1) == str(b2) == shape_name

    shape_command = shape_command_class(
        receiver=controller,
        start_x=-999, start_y=0,
        end_x=-999, end_y=100,
        color=(0, 0, 0)
    )
    preview_shape = copy.deepcopy(shape_command.shape)
    preview_shape.color = Color(0, 0, 0, 200)

    b1.mouse_move(controller, 10, 20, None)
    assert controller.command is None
    assert controller.preview is None

    b1.mouse_press(controller, -999, 0, Qt.LeftButton)
    b1.mouse_move(controller, -999, 100, None)
    assert controller.command is None
    assert controller.preview == preview_shape
    assert b1._start == (-999, 0)

    b1.mouse_press(controller, -999, 100, Qt.LeftButton)
    assert controller.command == shape_command
    assert controller.preview is None
    assert b1._start is None


def test_move_shape_brush(controller: ControllerMockup):
    b1 = MoveShapeBrush()
    b2 = MoveShapeBrush()
    assert b1 == b2
    assert str(b1) == str(b2) == 'Move'

    b1.mouse_move(controller, -1, 0, None)
    assert b1.cursor == Qt.ArrowCursor

    b1.mouse_move(controller, 0, 5, None)
    assert b1.cursor == Qt.OpenHandCursor

    b1.mouse_press(controller, 0, 0, Qt.LeftButton)
    assert controller.command is None
    assert b1.cursor == Qt.ClosedHandCursor

    b1.mouse_press(controller, 10, 10, Qt.LeftButton)
    assert controller.command == MoveShapeCommand(
        receiver=controller,
        start_x=0, start_y=0,
        end_x=10, end_y=10
    )
    assert b1._start is None
    assert b1.cursor == Qt.OpenHandCursor


def test_remove_shape_brush(controller: ControllerMockup):
    b1 = RemoveShapeBrush()
    b2 = RemoveShapeBrush()
    assert b1 == b2
    assert str(b1) == str(b2) == 'Remove'

    b1.mouse_move(controller, 1, 0, None)
    assert b1.cursor == Qt.ArrowCursor

    b1.mouse_move(controller, 0, 5, None)
    assert b1.cursor == Qt.PointingHandCursor

    b1.mouse_press(controller, 10, 10, Qt.LeftButton)
    assert controller.command == RemoveShapeCommand(receiver=controller, x=10, y=10)
