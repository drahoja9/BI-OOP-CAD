from app.gui import MainWindow
from app.commands import Command
from app.printers import CanvasPrinter
from app.shapes import Shape
from app.shapes_store import ShapesStore


class Controller:
    """
    Main class of this application. Holds all crucial pieces together.
    It represents a subject in the observer design pattern.
    """
    def __init__(self):
        self._gui = MainWindow(self)
        self._commands = []
        self._shapes = ShapesStore(self)
        self._printer = CanvasPrinter(self._gui.canvas)

    def add_shape(self, shape: Shape):
        self._shapes.add_shape(shape)

    def execute_command(self, command: Command):
        self._commands.append(command)
        command.execute()

    def print_all_shapes(self):
        self._shapes.print_all(self._printer)

    def update_canvas(self):
        # Emitting the QEvent.Paint event
        self._gui.canvas.update()

    def run_app(self):
        # Run the whole app
        self._gui.run()
