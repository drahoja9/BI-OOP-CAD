import copy
from typing import List

from app.shapes import Shape
from app.printers import Printer
from app.utils import Point


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
        self._notify()

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

    def add_shapes(self, *shapes: Shape):
        for shape in shapes:
            self._shapes.append(shape)
        self._notify()

    def remove_last_shape(self):
        try:
            self._shapes.pop()
            self._notify()
        except IndexError:
            pass

    def _remove_shapes(self, *shapes: Shape):
        try:
            for shape in shapes:
                self._shapes.remove(shape)
            self._notify()
        except ValueError:
            pass

    def remove_shapes_at(self, point: Point) -> List[Shape]:
        before_remove = copy.deepcopy(self._shapes)
        to_remove = []
        for shape in self._shapes:
            if shape.contains(point):
                to_remove.append(shape)
        self._remove_shapes(*to_remove)
        return before_remove

    def restart(self):
        self._shapes = []
        self._preview = None
        self._notify()
