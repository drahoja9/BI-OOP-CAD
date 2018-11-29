from typing import List

from app.shapes import Shape
from app.printers import Printer


class ShapesStore:
    """
    Holds together all the shapes and actions provided on them.
    """
    def __init__(self, controller, shapes: List[Shape] = None):
        super().__init__()
        self._shapes = shapes or []
        self._controller = controller

    def _notify(self):
        self._controller.update_canvas()

    def print_all(self, printer: Printer):
        for shape in self._shapes:
            shape.print_to(printer)

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
