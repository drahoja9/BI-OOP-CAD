import pytest
from PyQt5.QtCore import Qt

from app.canvas import Canvas
from app.brushes import LineShapeBrush, RectShapeBrush, DotShapeBrush, CircleShapeBrush
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
    canvas.set_color((10, 20, 30))
    assert canvas._brush is None

    canvas.set_brush(LineShapeBrush())
    assert canvas._brush.color == (10, 20, 30)
    assert canvas._brush == LineShapeBrush()

    canvas.set_brush(LineShapeBrush())
    assert canvas._brush is None

    canvas.set_brush(LineShapeBrush())
    assert canvas._brush.color == (10, 20, 30)
    assert canvas._brush == LineShapeBrush()

    canvas.set_brush(RectShapeBrush())
    assert canvas._brush.color == (10, 20, 30)
    assert canvas._brush == RectShapeBrush()


def test_set_color(canvas: Canvas):
    assert canvas.color == (0, 0, 0)

    canvas.set_brush(CircleShapeBrush())
    canvas.set_color((100, 200, 100))
    assert canvas.color == (100, 200, 100)
    assert canvas._brush.color == (100, 200, 100)


def test_mouse_move_event(canvas: Canvas):
    assert canvas._brush is None

    canvas.mouseMoveEvent(EventMockup)
    assert canvas._controller.command is None

    canvas.set_brush(DotShapeBrush())
    canvas.mouseMoveEvent(EventMockup)
    assert (
        canvas._controller.command
        ==
        PrintDotCommand(canvas._controller, EventMockup.x(), EventMockup.y(), (0, 0, 0))
    )


def test_mouse_press_event(canvas: Canvas):
    assert canvas._brush is None

    canvas.mousePressEvent(EventMockup)
    assert canvas._controller.command is None

    canvas.set_brush(RectShapeBrush())
    canvas.mousePressEvent(EventMockup)
    canvas.mousePressEvent(EventMockup)
    assert (
        canvas._controller.command
        ==
        PrintRectCommand(
            canvas._controller,
            EventMockup.x(), EventMockup.y(),
            EventMockup.x(), EventMockup.y(),
            (0, 0, 0)
        )
    )
