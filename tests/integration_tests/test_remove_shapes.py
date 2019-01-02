import io
from typing import Dict

from app.controller import Controller
from app.shapes import Shape


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
