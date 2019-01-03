import copy
from typing import List, Dict

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

    def _notify(self):
        self._controller.update()

    def is_empty(self) -> bool:
        return len(self._shapes) == 0

    def shapes_at(self, point: Point = None, divergence: bool = False) -> List[Shape]:
        if point:
            return [shape for shape in self._shapes if shape.contains(point, divergence)]
        else:
            return self._shapes

    def print_all(self, printer: Printer, point: Point = None) -> List[Shape]:
        printed = []
        # Order is important - first we want to print all stored shapes and after that the shape preview
        for shape in self._shapes:
            if point and shape.contains(point):
                shape.print_to(printer)
                printed.append(shape)
            elif not point:
                shape.print_to(printer)
                printed.append(shape)
        if self._preview is not None:
            self._preview.print_to(printer)

        return printed

    def set_preview(self, shape: Shape = None):
        self._preview = shape
        self._notify()

    def add_shapes(self, *shapes: Shape):
        for shape in shapes:
            self._shapes.append(copy.deepcopy(shape))
        self._notify()

    def move_shapes(self, move_from: Point, move_to: Point, divergence: bool = False) -> Dict[str, List[Shape]]:
        before_move = copy.deepcopy(self._shapes)
        moved = []
        to_remove = []
        for shape in self._shapes:
            if shape.contains(move_from, divergence):
                new_shape = shape.move(move_from, move_to)
                moved.append(new_shape)
                to_remove.append(shape)
        self._remove_shapes(*to_remove)
        self.add_shapes(*moved)
        return {'moved': moved, 'before_move': before_move}

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

    def remove_shapes_at(self, point: Point, divergence: bool = False) -> Dict[str, List[Shape]]:
        before_remove = copy.deepcopy(self._shapes)
        to_remove = []
        for shape in self._shapes:
            if shape.contains(point, divergence):
                to_remove.append(shape)
        self._remove_shapes(*to_remove)
        return {'removed': to_remove, 'before_remove': before_remove}

    def restart(self):
        self._shapes = []
        self._preview = None
        self._notify()
