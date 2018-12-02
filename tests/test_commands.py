import pytest
from PyQt5.QtGui import QColor

from app.commands import Command, PrintDotCommand, PrintLineCommand, PrintRectCommand, PrintCircleCommand
from app.shapes import Shape, Dot, Line, Rectangle, Circle
from app.utils import Point


class ReceiverMockup:
    def __init__(self):
        self.received = None

    def add_shape(self, shape: Shape):
        self.received = shape


@pytest.fixture
def receiver() -> ReceiverMockup:
    return ReceiverMockup()


def test_abstract_command():
    command = Command(None)

    with pytest.raises(NotImplementedError):
        command.execute()

    with pytest.raises(NotImplementedError):
        command.reverse()

    assert str(command) == 'Abstract command, should not be instantiated!'


def test_dot_command(receiver: ReceiverMockup):
    command = PrintDotCommand(receiver, 0, -12, (1, 2, 3))
    command.execute()
    assert receiver.received == Dot(Point(0, -12), QColor(1, 2, 3))
    assert str(command) == 'dot 0,-12'
    assert PrintDotCommand(receiver, 0, -12, (1, 2, 3)) == PrintDotCommand(receiver, 0, -12, (1, 2, 3))


def test_line_command(receiver: ReceiverMockup):
    command = PrintLineCommand(receiver, 10, 10, 20, 20, (100, 200, 100))
    command.execute()
    assert receiver.received == Line(Point(10, 10), Point(20, 20), QColor(100, 200, 100))
    assert str(command) == 'line 10,10 20,20'
    assert (
        PrintLineCommand(receiver, 10, 10, 20, 20, (100, 200, 100))
        ==
        PrintLineCommand(receiver, 10, 10, 20, 20, (100, 200, 100))
    )


def test_rect_command(receiver: ReceiverMockup):
    command = PrintRectCommand(receiver, 50, 50, 100, 100, (255, 255, 255))
    command.execute()
    assert receiver.received == Rectangle(Point(50, 50), 50, 50, QColor(255, 255, 255))
    assert str(command) == 'rect 50,50 50 50'
    assert (
        PrintRectCommand(receiver, 50, 50, 100, 100, (255, 255, 255))
        ==
        PrintRectCommand(receiver, 50, 50, 100, 100, (255, 255, 255))
    )


def test_circle_command(receiver: ReceiverMockup):
    # The circle is circumscribed inside a rectangle with top-left
    # corner at [0, 0] and bottom-right corner at [100, 100]
    command = PrintCircleCommand(receiver, 0, 0, 100, 100, (0, 0, 0))
    command.execute()
    assert receiver.received == Circle(Point(50, 50), 141, QColor(0, 0, 0))
    assert str(command) == 'circle 50,50 141'
    assert (
        PrintCircleCommand(receiver, 0, 0, 100, 100, (0, 0, 0))
        ==
        PrintCircleCommand(receiver, 0, 0, 100, 100, (0, 0, 0))
    )


def test_not_equals(receiver: ReceiverMockup):
    assert (
        PrintDotCommand(receiver, 0, 0, (0, 0, 0))
        !=
        PrintLineCommand(receiver, 0, 0, 0, 0, (0, 0, 0))
        !=
        PrintRectCommand(receiver, 0, 0, 0, 0, (0, 0, 0))
        !=
        PrintCircleCommand(receiver, 0, 0, 0, 0, (0, 0, 0))
    )
    assert (
        PrintDotCommand(receiver, 0, 0, (0, 0, 0))
        !=
        PrintDotCommand(receiver, 1, 0, (0, 0, 0))
    )
    assert (
        PrintLineCommand(receiver, 0, 0, 0, 0, (0, 0, 0))
        !=
        PrintLineCommand(receiver, 0, 0, 1, 0, (0, 0, 0))
    )
    assert (
        PrintRectCommand(receiver, 0, 0, 0, 0, (0, 0, 0))
        !=
        PrintRectCommand(receiver, 0, 1, 0, 0, (0, 0, 0))
    )
    assert (
        PrintCircleCommand(receiver, 0, 0, 0, 0, (0, 0, 0))
        !=
        PrintCircleCommand(receiver, 0, 0, 0, 1, (0, 0, 0))
    )
