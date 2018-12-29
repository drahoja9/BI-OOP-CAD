import io
from typing import List, Dict

from app.command_engine import CommandEngine
from app.commands import Command
from app.gui import MainWindow
from app.printers import CanvasPrinter, Printer, StreamTextPrinter
from app.shapes import Shape
from app.shapes_store import ShapesStore
from app.utils import Point


class Controller:
    """
    Main class of this application. Holds all crucial pieces together.
    It represents a subject in the observer design pattern.
    """

    def __init__(self):
        self._gui = MainWindow(self)
        self._command_engine = CommandEngine(self)
        self._printer = CanvasPrinter(self._gui.canvas)
        self._shapes = ShapesStore(self)

    def add_shapes(self, *shapes: Shape):
        for shape in shapes:
            self._gui.print_newline_to_history(str(shape))
        self._shapes.add_shapes(*shapes)

    def replace_shapes_store(self, shapes: List[Shape]):
        self._shapes = ShapesStore(self, shapes)
        self.update()

    def remove_last_shape(self):
        self._shapes.remove_last_shape()

    def remove_shapes_at(self, point: Point) -> Dict[str, List[Shape]]:
        return self._shapes.remove_shapes_at(point)

    def preview_shape(self, shape: Shape):
        self._shapes.set_preview(shape)

    def end_preview(self):
        self._shapes.set_preview(None)

    def execute_command(self, command: Command, from_redo: bool = False):
        self._gui.print_newline_to_history(' > ' + str(command))
        self._command_engine.execute_command(command, from_redo=from_redo)

    def remove_last_command(self):
        self._command_engine.remove_last_command()

    def delete_from_history(self, number_of_lines: int = 1):
        self._gui.delete_from_history(number_of_lines)

    def list_shapes(self, point: Point = None) -> List[Shape]:
        stream = io.StringIO()
        printed = self.print_all_shapes(StreamTextPrinter(stream), point)
        # Ignoring the last newline `\n`
        self._gui.print_newline_to_history(stream.getvalue()[:-1])
        return printed

    def print_all_shapes(self, printer: Printer = None, point: Point = None) -> List[Shape]:
        return self._shapes.print_all(printer or self._printer, point)

    def update(self):
        self._printer.update(self)

    def undo(self):
        self._command_engine.undo()

    def redo(self):
        self._command_engine.redo()

    def enable_undo(self):
        self._gui.enable_undo()

    def enable_redo(self):
        self._gui.enable_redo()

    def disable_undo(self):
        self._gui.disable_undo()

    def disable_redo(self):
        self._gui.disable_redo()

    def save(self, file: str):
        commands = self._command_engine.get_all_commands()
        with open(file, 'w+', encoding='utf-8') as f:
            f.write(f'{len(commands["redos"])}\n')
            [f.write(str(c) + '\n') for c in commands['undos']]
            [f.write(str(c) + '\n') for c in commands['redos']]

    def run_app(self):
        # Run the whole app
        self._gui.show()

    def restart(self):
        self._command_engine.restart()
        self._shapes.restart()
        self._gui.clear_history()
