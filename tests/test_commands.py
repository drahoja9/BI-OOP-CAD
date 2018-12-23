from typing import List

import pytest

from app.commands import Command, PrintDotCommand, PrintLineCommand, PrintRectCommand, PrintCircleCommand, \
    PrintPolylineCommand, RemoveShapeCommand, ListShapeCommand
from app.shapes import Shape, Dot, Line, Rectangle, Circle, Polyline
from app.utils import Point, Color


class ReceiverMockup:
    def __init__(self):
        self.shapes = [Dot(Point(10, 10), Color(0, 0, 0)), Line(Point(123, 321), Point(11, 11), Color(0, 0, 0))]
        self.received = None
        self.listed_shapes = None
        self.last_command_removed = None
        self.deleted_lines = 0

    def add_shapes(self, *shapes: Shape):
        if len(shapes) == 1:
            self.received = shapes[0]
        else:
            self.received = shapes

    def list_shapes(self, point: Point = None):
        to_list = []
        for shape in self.shapes:
            if point and shape.contains(point):
                to_list.append(shape)
            elif not point:
                to_list.append(shape)
        self.listed_shapes = to_list
        return to_list

    def replace_shapes_store(self, shapes: List[Shape]):
        self.received = shapes

    def remove_last_shape(self):
        self.received = None

    def remove_last_command(self):
        self.last_command_removed = True

    def remove_shapes_at(self, point: Point):
        self.received = point
        res = {'before_remove': self.shapes, 'removed': []}
        for shape in self.shapes:
            if shape.contains(point):
                res['removed'].append(shape)
        return res

    def delete_from_history(self, number_of_lines: int = 1):
        self.deleted_lines = number_of_lines


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
    assert str(command) == 'dot 0,-12 (1,2,3)'
    assert command == PrintDotCommand(receiver, 0, -12, (1, 2, 3))

    command.execute()
    assert receiver.received == Dot(Point(0, -12), Color(1, 2, 3))

    command.reverse()
    assert receiver.received is None
    assert receiver.deleted_lines == 2


def test_line_command(receiver: ReceiverMockup):
    command = PrintLineCommand(receiver, 10, 10, 20, 20, (100, 200, 100))
    assert str(command) == 'line 10,10 20,20 (100,200,100)'
    assert (
        command
        ==
        PrintLineCommand(receiver, 10, 10, 20, 20, (100, 200, 100))
    )

    command.execute()
    assert receiver.received == Line(Point(10, 10), Point(20, 20), Color(100, 200, 100))

    command.reverse()
    assert receiver.received is None
    assert receiver.deleted_lines == 2


def test_polyline_command(receiver: ReceiverMockup):
    command = PrintPolylineCommand(receiver, [(10, 10), (20, 20), (30, 30), (40, 20), (50, 10)], (100, 200, 255))
    assert str(command) == 'line 10,10 20,20 30,30 40,20 50,10 (100,200,255)'
    assert (
        command
        ==
        PrintPolylineCommand(receiver, [(10, 10), (20, 20), (30, 30), (40, 20), (50, 10)], (100, 200, 255))
    )

    command.execute()
    assert receiver.received == Polyline(
        Point(10, 10), Point(20, 20), Point(30, 30), Point(40, 20), Point(50, 10), color=Color(100, 200, 255)
    )

    command.reverse()
    assert receiver.received is None
    assert receiver.deleted_lines == 2


def test_rect_command(receiver: ReceiverMockup):
    command = PrintRectCommand(receiver, 50, 50, 100, 100, (255, 255, 255))
    assert str(command) == 'rect 50,50 50 50 (255,255,255)'
    assert (
        command
        ==
        PrintRectCommand(receiver, 50, 50, 100, 100, (255, 255, 255))
    )

    command.execute()
    assert receiver.received == Rectangle(Point(50, 50), 50, 50, Color(255, 255, 255))

    command.reverse()
    assert receiver.received is None
    assert receiver.deleted_lines == 2


def test_circle_command(receiver: ReceiverMockup):
    command = PrintCircleCommand(receiver, 0, 0, 100, 100, (0, 0, 0))
    assert str(command) == 'circle 0,0 141 (0,0,0)'
    assert (
        command
        ==
        PrintCircleCommand(receiver, 0, 0, 100, 100, (0, 0, 0))
    )

    command.execute()
    assert receiver.received == Circle(Point(0, 0), 141, Color(0, 0, 0))

    command.reverse()
    assert receiver.received is None
    assert receiver.deleted_lines == 2


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


def test_remove_shape_command(receiver: ReceiverMockup):
    command = RemoveShapeCommand(receiver, 123, 321)
    assert str(command) == 'remove 123,321'
    assert command == RemoveShapeCommand(receiver, 123, 321)

    command.execute()
    assert receiver.received == Point(123, 321)
    assert command._before_remove == [
        Dot(Point(10, 10), Color(0, 0, 0)),
        Line(Point(123, 321), Point(11, 11), Color(0, 0, 0))
    ]
    assert receiver.deleted_lines == 0

    command.reverse()
    assert receiver.received == [
        Dot(Point(10, 10), Color(0, 0, 0)),
        Line(Point(123, 321), Point(11, 11), Color(0, 0, 0))
    ]
    assert receiver.deleted_lines == 1

    command = RemoveShapeCommand(receiver, -1, -1)
    command.execute()
    assert receiver.deleted_lines == 1
    assert receiver.last_command_removed is True


def test_list_shape_command(receiver: ReceiverMockup):
    command = ListShapeCommand(receiver)
    assert str(command) == 'ls'
    assert command == ListShapeCommand(receiver)

    command.execute()
    assert receiver.listed_shapes == [
        Dot(Point(10, 10), Color(0, 0, 0)),
        Line(Point(123, 321), Point(11, 11), Color(0, 0, 0))
    ]
    assert command.listed == [
        Dot(Point(10, 10), Color(0, 0, 0)),
        Line(Point(123, 321), Point(11, 11), Color(0, 0, 0))
    ]
    command.reverse()
    assert receiver.deleted_lines == len(command.listed) + 1

    command = ListShapeCommand(receiver, 10, 10)
    assert str(command) == 'ls 10,10'
    assert command == ListShapeCommand(receiver, 10, 10)

    command.execute()
    assert receiver.listed_shapes == [
        Dot(Point(10, 10), Color(0, 0, 0)),
    ]
    assert command.listed == [
        Dot(Point(10, 10), Color(0, 0, 0)),
    ]
    command.reverse()
    assert receiver.deleted_lines == len(command.listed) + 1
