from typing import List, Tuple, Type

from app.shape_factory import ShapeFactory, PointsRectFactory, PointsCircleFactory
from app.shapes import Dot, Line, Rectangle, Circle, Polyline
from app.utils import Point, Color


class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def __str__(self):
        return 'Abstract command, should not be instantiated!'

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.receiver == other.receiver


# -------------------------------------------------- Shape commands ---------------------------------------------------


class ShapeCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)
        self.shape = None

    def execute(self):
        self.receiver.add_shapes(self.shape)

    def reverse(self):
        self.receiver.remove_last_shape()
        self.receiver.delete_from_history(2)

    def __eq__(self, other):
        return super().__eq__(other) and self.shape == other.shape

    def __str__(self):
        return f' ({self.shape.color.r},{self.shape.color.g},{self.shape.color.b})'


class PrintDotCommand(ShapeCommand):
    def __init__(self, receiver, x: int, y: int, color: tuple):
        super().__init__(receiver)
        self.shape = Dot(
            Point(x, y),
            Color(*color)
        )

    def __str__(self):
        return f'dot {self.shape.start.x},{self.shape.start.y}' + super().__str__()


class PrintLineCommand(ShapeCommand):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int, color: tuple):
        super().__init__(receiver)
        self.shape = Line(
            Point(start_x, start_y),
            Point(end_x, end_y),
            Color(*color)
        )

    def __str__(self):
        return (f'line {self.shape.start.x},{self.shape.start.y} {self.shape.end.x},{self.shape.end.y}' +
                super().__str__())


class PrintPolylineCommand(ShapeCommand):
    def __init__(self, receiver, points: List[Tuple[int, int]], color: tuple):
        super().__init__(receiver)
        points_ = []
        for point in points:
            points_.append(Point(point[0], point[1]))
        self.shape = Polyline(*points_, color=Color(*color))

    def __str__(self):
        res = f'line'
        for point in self.shape.get_props():
            res += f' {point.x},{point.y}'
        return res + super().__str__()


class PrintRectCommand(ShapeCommand):
    def __init__(self, receiver, start_x: int, start_y: int, color: Tuple[int, int, int],
                 rect_factory: Type[ShapeFactory] = PointsRectFactory, **kwargs):
        super().__init__(receiver)
        self.shape: Rectangle = rect_factory.get_shape(start_x, start_y, color, **kwargs)

    def __str__(self):
        return (f'rect {self.shape.start.x},{self.shape.start.y} {self.shape.width} {self.shape.height}' +
                super().__str__())


class PrintCircleCommand(ShapeCommand):
    def __init__(self, receiver, start_x: int, start_y: int, color: Tuple[int, int, int],
                 circle_factory: Type[ShapeFactory] = PointsCircleFactory, **kwargs):
        super().__init__(receiver)
        self.shape: Circle = circle_factory.get_shape(start_x, start_y, color, **kwargs)

    def __str__(self):
        return f'circle {self.shape.start.x},{self.shape.start.y} {self.shape.radius}' + super().__str__()


# -------------------------------------------------- Other commands ---------------------------------------------------


class MoveShapeCommand(Command):
    def __init__(self, receiver, start_x: int, start_y: int, end_x: int, end_y: int):
        super().__init__(receiver)
        self.start = Point(start_x, start_y)
        self.end = Point(end_x, end_y)
        self._before_move = []

    def execute(self):
        res = self.receiver.move_shapes(self.start, self.end)
        self._before_move = res['before_move']
        # If nothing was moved, there's no need to keep empty move command in command engine
        if not res['moved']:
            self.receiver.remove_last_command()
            self.receiver.delete_from_history(1)

    def reverse(self):
        if self._before_move:
            self.receiver.replace_shapes_store(self._before_move)
            self.receiver.delete_from_history(1)

    def __eq__(self, other):
        return super().__eq__(other) and self.start == other.start and self.end == other.end

    def __str__(self):
        return f'move {self.start.x},{self.start.y} {self.end.x},{self.end.y}'


class RemoveShapeCommand(Command):
    def __init__(self, receiver, x: int, y: int):
        super().__init__(receiver)
        self.point = Point(x, y)
        self._before_remove = []

    def execute(self):
        res = self.receiver.remove_shapes_at(self.point)
        self._before_remove = res['before_remove']
        # If nothing was removed, there's no need to keep empty remove command in command engine
        if not res['removed']:
            self.receiver.remove_last_command()
            self.receiver.delete_from_history(1)

    def reverse(self):
        if self._before_remove:
            self.receiver.replace_shapes_store(self._before_remove)
            self.receiver.delete_from_history(1)

    def __eq__(self, other):
        return super().__eq__(other) and self.point == other.point

    def __str__(self):
        return f'remove {self.point.x},{self.point.y}'


class ListShapeCommand(Command):
    def __init__(self, receiver, x: int = None, y: int = None):
        super().__init__(receiver)
        self.listed = []
        if x and y:
            self.point = Point(x, y)
        else:
            self.point = None

    def execute(self):
        self.listed = self.receiver.print_shapes_to_history(self.point)

    def reverse(self):
        if self.listed:
            self.receiver.delete_from_history(len(self.listed) + 1)

    def __eq__(self, other):
        return super().__eq__(other) and self.point == other.point

    def __str__(self):
        if self.point:
            return f'ls {self.point.x},{self.point.y}'
        else:
            return 'ls'


class ClearCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)
        self.shapes = []

    def execute(self):
        self.shapes = self.receiver.shapes_at(None)
        self.receiver.restart()

    def reverse(self):
        self.receiver.delete_from_history(1)
        self.receiver.replace_shapes_store(self.shapes)

    def __eq__(self, other):
        return super().__eq__(other) and self.shapes == other.shapes

    def __str__(self):
        return 'clear'


class InvalidCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def execute(self):
        self.receiver.print_to_history('Invalid command!')

    def reverse(self):
        self.receiver.delete_from_history(2)

    def __str__(self):
        return 'invalid command'
