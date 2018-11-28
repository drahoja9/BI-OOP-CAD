from typing import List

from app.shapes import Shape
from app.printers import Printer


class ShapesStore:
    def __init__(self, printer: Printer, shapes: List[Shape] = None):
        super().__init__()
        self._shapes = shapes or []
        self._printer = printer

    def print_all_shapes(self):
        self._printer.print_all(self._shapes)

    def add_shape(self, shape: Shape):
        self._shapes.append(shape)
        self.print_all_shapes()

    def add_shapes(self, *shapes: Shape):
        for shape in shapes:
            self.add_shape(shape)

    def remove_last_shape(self):
        try:
            self._shapes.pop()
            self.print_all_shapes()
        except IndexError:
            pass

    def remove_shape(self, shape: Shape):
        try:
            self._shapes.remove(shape)
            self.print_all_shapes()
        except ValueError:
            pass
