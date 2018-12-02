import pytest

from app.canvas import Canvas
from app.brushes import LineBrush, RectBrush, DotBrush
from app.commands import Command, PrintDotCommand, PrintRectCommand
from app.gui import MainWindow


class ControllerMockup:
    def __init__(self):
        self.all_shapes = None
        self.command = None

    def print_all_shapes(self):
        self.all_shapes = 'all'

    def execute_command(self, command: Command):
        self.command = command


class EventMockup:
    @staticmethod
    def x() -> int:
        return 10

    @staticmethod
    def y() -> int:
        return 20


@pytest.fixture(scope='module')
def canvas() -> Canvas:
    controller = ControllerMockup()
    gui = MainWindow(controller)
    canvas = Canvas(controller)
    return canvas


def test_set_brush(canvas: Canvas):
    assert canvas._brush is None

    canvas.set_brush(LineBrush)
    assert canvas._brush == LineBrush

    canvas.set_brush(LineBrush)
    assert canvas._brush is None

    canvas.set_brush(LineBrush)
    assert canvas._brush == LineBrush

    canvas.set_brush(RectBrush)
    assert canvas._brush == RectBrush


def test_pain_event(canvas: Canvas):
    canvas.paintEvent(EventMockup)
    assert canvas._controller.all_shapes == 'all'


def test_mouse_move_event(canvas: Canvas):
    canvas.set_brush(RectBrush)
    assert canvas._brush is None

    canvas.mouseMoveEvent(EventMockup)
    assert canvas._controller.command is None

    canvas.set_brush(DotBrush)
    canvas.mouseMoveEvent(EventMockup)
    assert (
        canvas._controller.command
        ==
        PrintDotCommand(canvas._controller, EventMockup.x(), EventMockup.y(), (0, 0, 0))
    )


def test_mouse_press_event(canvas: Canvas):
    canvas.set_brush(RectBrush)
    canvas.set_brush(RectBrush)
    assert canvas._start is None
    assert canvas._brush is None

    canvas.mousePressEvent(EventMockup)
    assert canvas._start is None

    canvas.set_brush(RectBrush)
    canvas.mousePressEvent(EventMockup)
    assert canvas._start == (EventMockup.x(), EventMockup.y())

    canvas.mousePressEvent(EventMockup)
    assert canvas._start is None
    assert (
        canvas._controller.command
        ==
        PrintRectCommand(
            canvas._controller,
            EventMockup.x(), EventMockup.y(),
            EventMockup.x(), EventMockup.y(),
            (255, 255, 255)
        )
    )
