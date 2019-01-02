import io
from typing import Dict

from app.commands import PrintRectCommand
from app.controller import Controller
from app.shape_factory import DimensionsRectFactory
from app.shapes import Shape, Polyline, Rectangle
from app.utils import Point, Color


def test_move_shapes(controller: Controller, shape_commands, commands, stream: io.StringIO, shapes: Dict[str, Shape]):
    for command in shape_commands:
        controller.execute_command(command)

    rect = Rectangle(top_left=Point(10, 10), width=10, height=10, color=Color(10, 20, 30))
    moved_rect = Rectangle(top_left=Point(-10, 20), width=rect.width, height=rect.height, color=rect.color)
    moved_polyline = Polyline(Point(-10, 20), Point(0, 30), Point(10, 20), color=shapes['polyline'].color)
    rect_command = PrintRectCommand(
        receiver=controller,
        start_x=rect.start.x, start_y=rect.start.y,
        color=rect.color,
        rect_factory=DimensionsRectFactory,
        width=rect.width,
        height=rect.height
    )
    controller.execute_command(rect_command)

    controller.execute_command(commands[4])
    assert controller._shapes._shapes == [
        shapes['dot'],
        shapes['line'],
        shapes['rectangle'],
        shapes['circle'],
        moved_polyline,
        moved_rect
    ]
    assert controller._command_engine._undos == [
        *shape_commands,
        rect_command,
        commands[4]
    ]
    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {shape_commands[3]}\n{shapes["rectangle"]}\n'
        f' > {shape_commands[4]}\n{shapes["circle"]}\n'
        f' > {rect_command}\n{rect}\n'
        f' > {commands[4]}'
    )
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{rect}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{moved_polyline}\n{moved_rect}\n'
    )
    assert stream.getvalue() == res

    controller.execute_command(commands[5])
    assert controller._shapes._shapes == [
        shapes['dot'],
        shapes['line'],
        shapes['rectangle'],
        shapes['circle'],
        moved_polyline,
        moved_rect
    ]
    assert controller._command_engine._undos == [
        *shape_commands,
        rect_command,
        commands[4]
    ]
    assert controller._gui._ui.history.toPlainText() == (
        f' > {shape_commands[0]}\n{shapes["dot"]}\n'
        f' > {shape_commands[1]}\n{shapes["line"]}\n'
        f' > {shape_commands[2]}\n{shapes["polyline"]}\n'
        f' > {shape_commands[3]}\n{shapes["rectangle"]}\n'
        f' > {shape_commands[4]}\n{shapes["circle"]}\n'
        f' > {rect_command}\n{rect}\n'
        f' > {commands[4]}'
    )
    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{rect}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{moved_polyline}\n{moved_rect}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{moved_polyline}\n{moved_rect}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n{moved_polyline}\n{moved_rect}\n'
    )
    assert stream.getvalue() == res
