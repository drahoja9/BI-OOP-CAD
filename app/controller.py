from typing import List, Dict

from app.command_engine import CommandEngine
from app.commands import Command
from app.gui import MainWindow
from app.printers import CanvasPrinter, Printer
from app.shapes import Shape
from app.shapes_store import ShapesStore
from app.utils import Point
from app.parsers.color_parser import RgbColorParser


class Controller:
    """
    Main class of this application. Holds all crucial pieces together.
    It represents an observer in the observer design pattern.
    """

    def __init__(self):
        self._gui = MainWindow(self)
        self._command_engine = CommandEngine(self)
        self._printer = CanvasPrinter(self._gui.canvas)
        self._shapes = ShapesStore(self)

        # import CliParser this late to avoid import loop
        from app.parsers.cli_parser import CliParser
        self._cli_parser = CliParser(self, RgbColorParser())

    def add_shapes(self, *shapes: Shape):
        for shape in shapes:
            self.print_to_history(str(shape))
        self._shapes.add_shapes(*shapes)

    def move_shapes(self, move_from: Point, move_to: Point, divergence: bool = False) -> Dict[str, List[Shape]]:
        return self._shapes.move_shapes(move_from, move_to, divergence)

    def replace_shapes_store(self, shapes: List[Shape]):
        self._shapes = ShapesStore(self, shapes)
        self.update()

    def remove_last_shape(self):
        self._shapes.remove_last_shape()

    def remove_shapes_at(self, point: Point, divergence: bool = False) -> Dict[str, List[Shape]]:
        return self._shapes.remove_shapes_at(point, divergence)

    def preview_shape(self, shape: Shape):
        self._shapes.set_preview(shape)

    def end_preview(self):
        self._shapes.set_preview(None)

    def parse_command(self, command_text: str):
        command = self._cli_parser.parse_input(command_text)
        self.execute_command(command, command_text=command_text)

    def execute_command(self, command: Command, from_redo: bool = False, command_text: str = None):
        history_line = ' > ' + (command_text or str(command))
        self._gui.print_lines_to_history(history_line)
        self._command_engine.execute_command(command, from_redo=from_redo)

    def remove_last_command(self):
        self._command_engine.remove_last_command()

    def print_to_history(self, lines: str):
        self._gui.print_lines_to_history(lines)

    def delete_from_history(self, number_of_lines: int = 1):
        self._gui.delete_from_history(number_of_lines)

    def shapes_at(self, point: Point = None, divergence: bool = False) -> List[Shape]:
        return self._shapes.shapes_at(point, divergence)

    def print_shapes_to_history(self, point: Point):
        for shape in self.shapes_at(point):
            self.print_to_history(str(shape))

    def print_all_shapes(self, printer: Printer = None) -> List[Shape]:
        return self._shapes.print_all(printer or self._printer)

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

    def save_dialog(self, path_to_file: str):
        self._gui.save_dialog(path_to_file)

    def load_dialog(self, path_to_file: str):
        self._gui.load_dialog(path_to_file)

    def save(self, file: str):
        commands = self._command_engine.get_all_commands()
        with open(file, 'w+', encoding='utf-8') as f:
            [f.write(str(c) + '\n') for c in commands['undos']]

        self._gui.set_status('File saved!')

    def load(self, file: str):
        with open(file, 'r', encoding='utf-8') as f:
            # Getting rid of the newline `\n` at the end of every line
            commands = [line[:-1] for line in f.readlines()]
            for command_text in commands:
                command = self._cli_parser.parse_input(command_text)
                self.execute_command(command, command_text=command_text)

        self._gui.set_status('File loaded!')

    def run_app(self):
        # Run the whole app
        self._gui.show()

    def clear_dialog(self) -> bool:
        return self._gui.clear_dialog()

    def restart(self):
        self._shapes.restart()

    def quit(self):
        self._gui.close()
