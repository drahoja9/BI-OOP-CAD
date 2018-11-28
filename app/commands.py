from typing import List, Tuple

from PyQt5.QtGui import QColor

from app.shapes_store import ShapesStore
from app.shapes import Shape, Dot, Line, Rectangle, Circle
from app.utils import Point


class Command:
    def __init__(self, receiver):
        self._receiver = receiver

    def execute(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError


class PrintDotCommand(Command):
    def __init__(self, receiver: ShapesStore, x: int, y: int, color: Tuple[int, int, int]):
        super().__init__(receiver)
        self._dot = Dot(Point(x, y), QColor(*color))

    def execute(self):
        self._receiver.add_shape(self._dot)

    def reverse(self) -> Command:
        pass


# class PrintRectCommand(Command):
#     def __init__(self, receiver: ShapesStore, shape: Shape):
#         super().__init__(receiver)
#         self._shape = shape
#
#     def execute(self):
#         self._receiver.add_shape(self._shape)
#
#     def reverse(self) -> Command:
#         pass


class CommandEngine:
    def __init__(self, commands: List[Command] = None):
        self._commands = commands or []

    def store_command(self, command: Command):
        self._commands.append(command)

    def execute_all_commands(self):
        for command in self._commands:
            command.execute()
