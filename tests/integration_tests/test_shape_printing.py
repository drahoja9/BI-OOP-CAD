import io
from typing import Dict, Tuple

import pytest
from pytestqt.qtbot import QtBot

from app.commands import PrintDotCommand, PrintLineCommand, PrintPolylineCommand, PrintRectCommand, PrintCircleCommand, \
    Command, RemoveShapeCommand, ListShapeCommand
from app.controller import Controller
from app.printers import StreamTextPrinter
from app.shapes import Shape


@pytest.fixture
def stream() -> io.StringIO:
    stream = io.StringIO()
    return stream


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
        end_x=-123, end_y=321,
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
def commands(controller: Controller) -> Tuple[Command, Command, Command, Command]:
    c1 = RemoveShapeCommand(receiver=controller, x=10, y=10)
    c2 = RemoveShapeCommand(receiver=controller, x=-10, y=-10)
    c3 = ListShapeCommand(receiver=controller)
    c4 = ListShapeCommand(receiver=controller, x=0, y=0)
    return c1, c2, c3, c4


def test_shape_printing(controller: Controller, shape_commands, stream: io.StringIO, shapes: Dict[str, Shape]):
    for command in shape_commands:
        controller.execute_command(command)

    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {shape_commands[3]}\n{shapes["rectangle"]}\n'
        f' > {shape_commands[4]}\n{shapes["circle"]}'
    )
    assert controller._command_engine._undos == [
        shape_commands[0],
        shape_commands[1],
        shape_commands[2],
        shape_commands[3],
        shape_commands[4],
    ]
    assert controller._shapes._shapes == [*shapes.values()]

    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
    )
    assert stream.getvalue() == res


def test_undo_redo(controller: Controller, shape_commands, stream: io.StringIO, shapes: Dict[str, Shape]):
    for command in shape_commands:
        controller.execute_command(command)
    assert controller._command_engine._redos == []
    assert controller._gui._ui.actionUndo.isEnabled() is True
    assert controller._gui._ui.actionRedo.isEnabled() is False

    for i in range(len(shape_commands)):
        controller.undo()
    assert controller._command_engine._undos == []
    assert controller._command_engine._redos == [
        shape_commands[4],
        shape_commands[3],
        shape_commands[2],
        shape_commands[1],
        shape_commands[0],
    ]
    assert controller._shapes._shapes == []
    assert controller._gui._ui.actionUndo.isEnabled() is False
    assert controller._gui._ui.actionRedo.isEnabled() is True
    assert controller._gui._ui.history.toPlainText() == ''
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n'
    )
    assert stream.getvalue() == res

    controller.redo()
    controller.redo()
    assert controller._command_engine._undos == [
        shape_commands[0],
        shape_commands[1]
    ]
    assert controller._command_engine._redos == [
        shape_commands[4],
        shape_commands[3],
        shape_commands[2]
    ]
    assert controller._shapes._shapes == [
        shapes['dot'],
        shapes['line']
    ]
    assert controller._gui._ui.actionUndo.isEnabled() is True
    assert controller._gui._ui.actionRedo.isEnabled() is True
    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}'
    )
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
    )
    assert stream.getvalue() == res

    controller.execute_command(shape_commands[0])
    assert controller._command_engine._undos == [
        shape_commands[0],
        shape_commands[1],
        shape_commands[0]
    ]
    assert controller._command_engine._redos == []
    assert controller._shapes._shapes == [
        shapes['dot'],
        shapes['line'],
        shapes['dot']
    ]
    assert controller._gui._ui.actionUndo.isEnabled() is True
    assert controller._gui._ui.actionRedo.isEnabled() is False
    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}\n'
        f' > {shape_commands[0]}\n{shapes["dot"]}'
    )
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["dot"]}\n'
    )
    assert stream.getvalue() == res


def test_remove_shapes(controller: Controller, shape_commands, commands, stream: io.StringIO, shapes: Dict[str, Shape]):
    for command in shape_commands:
        controller.execute_command(command)
    controller.execute_command(shape_commands[2])

    controller.execute_command(commands[0])
    assert controller._shapes._shapes == [
        shapes['dot'],
        shapes['line'],
        shapes['rectangle'],
        shapes['circle']
    ]
    assert controller._command_engine._undos == [
        *shape_commands,
        shape_commands[2],
        commands[0]
    ]
    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {shape_commands[3]}\n{shapes["rectangle"]}\n'
        f' > {shape_commands[4]}\n{shapes["circle"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {commands[0]}'
    )
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
    )
    assert stream.getvalue() == res

    controller.execute_command(commands[1])
    assert controller._shapes._shapes == [
        shapes['dot'],
        shapes['line'],
        shapes['rectangle'],
        shapes['circle']
    ]
    assert controller._command_engine._undos == [
        *shape_commands,
        shape_commands[2],
        commands[0]
    ]
    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {shape_commands[3]}\n{shapes["rectangle"]}\n'
        f' > {shape_commands[4]}\n{shapes["circle"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {commands[0]}'
    )
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
    )
    assert stream.getvalue() == res

    controller.undo()
    assert controller._shapes._shapes == [*shapes.values(), shapes['polyline']]
    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {shape_commands[3]}\n{shapes["rectangle"]}\n'
        f' > {shape_commands[4]}\n{shapes["circle"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}'
    )
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{shapes["polyline"]}\n'
    )
    assert stream.getvalue() == res
