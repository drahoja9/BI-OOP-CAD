import io
from typing import Tuple

import pytest
from pytestqt.qtbot import QtBot

from app.commands import Command, PrintDotCommand, PrintLineCommand, PrintPolylineCommand, PrintRectCommand, \
    PrintCircleCommand, RemoveShapeCommand, ListShapeCommand, MoveShapeCommand
from app.controller import Controller
from app.printers import StreamTextPrinter


@pytest.fixture
def stream() -> io.StringIO:
    return io.StringIO()


@pytest.fixture
def controller(qtbot: QtBot, stream: io.StringIO) -> Controller:
    controller = Controller()
    printer = StreamTextPrinter(stream)
    controller._printer = printer
    controller.run_app()
    qtbot.addWidget(controller._gui)
    return controller


@pytest.fixture
def shape_commands(controller: Controller) -> Tuple[Command, Command, Command, Command, Command]:
    c1 = PrintDotCommand(receiver=controller, x=10, y=200000000, color=(1, 2, 3))
    c2 = PrintLineCommand(
        receiver=controller,
        start_x=1000, start_y=-1000,
        end_x=0, end_y=-1000,
        color=(0, 0, 0)
    )
    c3 = PrintPolylineCommand(
        receiver=controller,
        points=[(10, 10), (20, 20), (30, 10)],
        color=(48, 210, 111)
    )
    c4 = PrintRectCommand(
        receiver=controller,
        start_x=0, start_y=0,
        end_x=1, end_y=50000,
        color=(255, 255, 255)
    )
    c5 = PrintCircleCommand(
        receiver=controller,
        start_x=12345, start_y=54321,
        end_x=13344, end_y=54321,
        color=(123, 255, 0)
    )
    return c1, c2, c3, c4, c5


@pytest.fixture
def commands(controller: Controller) -> Tuple[Command, Command, Command, Command, Command, Command]:
    c1 = RemoveShapeCommand(receiver=controller, x=10, y=10)
    c2 = RemoveShapeCommand(receiver=controller, x=-10, y=-10)
    c3 = ListShapeCommand(receiver=controller)
    c4 = ListShapeCommand(receiver=controller, x=0, y=0)
    c5 = MoveShapeCommand(receiver=controller, start_x=10, start_y=10, end_x=-10, end_y=20)
    c6 = MoveShapeCommand(receiver=controller, start_x=-10, start_y=-10, end_x=-10, end_y=20)
    return c1, c2, c3, c4, c5, c6
