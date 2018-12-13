from typing import List

from app.shapes import Shape
from app.printers import Printer


class ShapesStore:
    """
    Holds together all the shapes and actions provided on them.
    When anything changes, notifies the main controller (so in a way,
    this is a subject and the controller is its observer, right?).
    """

    def __init__(self, controller, shapes: List[Shape] = None):
        super().__init__()
        self._shapes = shapes or []
        self._controller = controller
        self._preview = None

    def _notify(self):
        self._controller.update_canvas()

    def is_empty(self) -> bool:
        return len(self._shapes) == 0

    def print_all(self, printer: Printer):
        # Order is important - first we want to print all stored shapes and after that the shape preview
        for shape in self._shapes:
            shape.print_to(printer)
        if self._preview is not None:
            self._preview.print_to(printer)

    def set_preview(self, shape: Shape = None):
        self._preview = shape
        self._notify()

    def add_shape(self, shape: Shape):
        self._shapes.append(shape)
        self._notify()

    def add_shapes(self, *shapes: Shape):
        for shape in shapes:
            self.add_shape(shape)

    def remove_last_shape(self):
        try:
            self._shapes.pop()
            self._notify()
        except IndexError:
            pass

    def remove_shape(self, shape: Shape):
        try:
            self._shapes.remove(shape)
            self._notify()
        except ValueError:
            pass
