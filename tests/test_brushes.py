import pytest

from app.brushes import Brush, DotBrush, LineBrush, RectBrush, CircleBrush
from app.commands import PrintDotCommand, PrintLineCommand, PrintRectCommand, PrintCircleCommand, Command


class ControllerMockup:
    def __init__(self):
        self.command = None

    def execute_command(self, command: Command):
        self.command = command


@pytest.fixture
def controller() -> ControllerMockup:
    return ControllerMockup()


def test_abstract_brush():
    b1 = Brush()
    b2 = Brush()
    assert b1 == b2


def test_dot_brush(controller: ControllerMockup):
    b1 = DotBrush()
    b2 = DotBrush()
    assert b1 == b2

    b1.mouse_move(controller, 10, 20)
    assert controller.command == PrintDotCommand(controller, 10, 20, (0, 0, 0))

    b1.mouse_press(controller, 123, 321)
    assert controller.command == PrintDotCommand(controller, 123, 321, (0, 0, 0))


def test_line_brush(controller: ControllerMockup):
    b1 = LineBrush()
    b2 = LineBrush()
    assert b1 == b2

    b1.mouse_move(controller, 10, 20)
    assert controller.command is None

    b1.mouse_press(controller, -999, 0)
    b1.mouse_press(controller, 0, -999)
    assert controller.command == PrintLineCommand(controller, -999, 0, 0, -999, (255, 255, 255))


def test_rect_brush(controller: ControllerMockup):
    b1 = RectBrush()
    b2 = RectBrush()
    assert b1 == b2

    b1.mouse_move(controller, 10, 20)
    assert controller.command is None

    b1.mouse_press(controller, 99, 10)
    b1.mouse_press(controller, 10, -10)
    assert controller.command == PrintRectCommand(controller, 99, 10, 10, -10, (255, 255, 255))


def test_circle_brush(controller: ControllerMockup):
    b1 = CircleBrush()
    b2 = CircleBrush()
    assert b1 == b2

    b1.mouse_move(controller, 10, 20)
    assert controller.command is None

    b1.mouse_press(controller, 1, 1)
    b1.mouse_press(controller, 2, 2)
    assert controller.command == PrintCircleCommand(controller, 1, 1, 2, 2, (255, 255, 255))
