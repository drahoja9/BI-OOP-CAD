import io
from typing import Dict

from app.controller import Controller
from app.shapes import Shape


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
