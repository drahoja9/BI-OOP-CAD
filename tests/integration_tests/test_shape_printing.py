import io
from typing import Dict

from pytestqt.qtbot import QtBot

from app.commands import PrintDotCommand, PrintLineCommand, PrintPolylineCommand, PrintRectCommand, PrintCircleCommand
from app.controller import Controller
from app.printers import StreamTextPrinter
from app.shapes import Shape


def test_shape_printing(qtbot: QtBot, shapes: Dict[str, Shape]):
    controller = Controller()
    stream = io.StringIO()
    printer = StreamTextPrinter(stream)
    controller._printer = printer
    controller.run_app()
    qtbot.addWidget(controller._gui)

    c1 = PrintDotCommand(controller, 10, 200000000, (1, 2, 3))
    c2 = PrintLineCommand(controller, 1000, -1000, -123, 321, (0, 0, 0))
    c3 = PrintPolylineCommand(controller, [(10, 10), (20, 20), (30, 10)], (48, 210, 111))
    c4 = PrintRectCommand(controller, 0, 0, 1, 50000, (255, 255, 255))
    c5 = PrintCircleCommand(controller, 12345, 54321, 13344, 54321, (123, 255, 0))

    controller.execute_command(c1)
    controller.execute_command(c2)
    controller.execute_command(c3)
    controller.execute_command(c4)
    controller.execute_command(c5)

    assert controller._gui._ui.history.text() == (
        f' > {c1}\n{shapes["dot"]}\n'
        f' > {c2}\n{shapes["line"]}\n'
        f' > {c3}\n{shapes["polyline"]}\n'
        f' > {c4}\n{shapes["rectangle"]}\n'
        f' > {c5}\n{shapes["circle"]}\n'
    )
    assert controller._command_engine._undos == [c1, c2, c3, c4, c5]
    assert controller._shapes._shapes == [*shapes.values()]

    res = (
        f'{shapes["dot"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n'
        f'{shapes["dot"]}\n{shapes["line"]}\n{shapes["polyline"]}\n{shapes["rectangle"]}\n{shapes["circle"]}\n'
    )
    assert stream.getvalue() == res
