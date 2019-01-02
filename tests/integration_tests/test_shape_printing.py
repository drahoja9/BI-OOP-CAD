import io
from typing import Dict

from app.controller import Controller
from app.shapes import Shape


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
