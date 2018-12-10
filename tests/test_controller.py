from typing import Dict
import io

import pytest

from app.controller import Controller
from app.shapes import Shape
from app.commands import Command
from app.printers import StreamTextPrinter


class CommandMockup(Command):
    def __init__(self):
        super().__init__(None)
        self.executed = False

    def execute(self):
        self.executed = True

    def reverse(self):
        pass


class CanvasMockup:
    def __init__(self):
        self.updated = False

    def update(self):
        self.updated = True


@pytest.fixture()
def controller(qtbot) -> Controller:
    controller = Controller()
    controller.run_app()
    qtbot.addWidget(controller._gui)
    yield controller


def test_add_shape(controller: Controller, shapes: Dict[str, Shape]):
    assert controller._shapes.is_empty() is True

    controller.add_shape(shapes['circle'])
    assert controller._shapes._shapes[0] == shapes['circle']


def test_execute_command(controller: Controller):
    assert controller._commands == []
    command = CommandMockup()
    controller.execute_command(command)
    assert controller._commands[0] == command
    assert command.executed is True


def test_print_all_shapes(controller: Controller, shapes: Dict[str, Shape]):
    stream = io.StringIO()
    printer = StreamTextPrinter(stream)
    controller._printer = printer

    controller.add_shape(shapes['circle'])
    controller.add_shape(shapes['rectangle'])
    controller.print_all_shapes()
    # The last line is also ended with a `\n`
    lines = stream.getvalue().split('\n')[:-1]
    assert lines[0] == str(shapes['circle'])
    assert lines[1] == str(shapes['rectangle'])


def test_update_canvas(controller: Controller):
    canvas = CanvasMockup()
    assert canvas.updated is False
    controller._gui.canvas = canvas
    controller.update_canvas()
    assert canvas.updated is True


def test_restart(controller: Controller, shapes: Dict[str, Shape]):
    controller.add_shape(shapes['line'])
    controller.add_shape(shapes['rectangle'])
    c1 = CommandMockup()
    c2 = CommandMockup()
    controller.execute_command(c1)
    controller.execute_command(c2)
    assert controller._shapes._shapes == [shapes['line'], shapes['rectangle']]
    assert controller._commands == [c1, c2]

    canvas = CanvasMockup()
    controller._gui.canvas = canvas
    assert canvas.updated is False
    controller.restart()
    assert controller._shapes.is_empty() is True
    assert controller._commands == []
    assert canvas.updated is True
