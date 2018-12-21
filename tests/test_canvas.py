import pytest
from PyQt5.QtCore import Qt

from app.canvas import Canvas
from app.brushes import LineBrush, RectBrush, DotBrush
from app.commands import Command, PrintDotCommand, PrintRectCommand
from app.gui import MainWindow


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
    return canvas


def test_set_brush(canvas: Canvas):
    assert canvas.brush is None

    canvas.set_brush(LineBrush())
    assert canvas.brush == LineBrush()

    canvas.set_brush(RectBrush())
    assert canvas.brush == RectBrush()


def test_pain_event(canvas: Canvas):
    canvas.paintEvent(EventMockup)
    assert canvas._controller.all_shapes == 'printed all shapes'


def test_mouse_move_event(canvas: Canvas):
    assert canvas.brush is None

    canvas.mouseMoveEvent(EventMockup)
    assert canvas._controller.command is None

    canvas.set_brush(DotBrush())
    canvas.mouseMoveEvent(EventMockup)
    assert (
        canvas._controller.command
        ==
        PrintDotCommand(canvas._controller, EventMockup.x(), EventMockup.y(), (0, 0, 0))
    )


def test_mouse_press_event(canvas: Canvas):
    assert canvas.brush is None

    canvas.mousePressEvent(EventMockup)
    assert canvas._controller.command is None

    canvas.set_brush(RectBrush())
    canvas.mousePressEvent(EventMockup)
    canvas.mousePressEvent(EventMockup)
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
