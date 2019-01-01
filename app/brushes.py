import math

from PyQt5.QtCore import Qt

from app.commands import PrintLineCommand, PrintRectCommand, PrintCircleCommand, PrintDotCommand, PrintPolylineCommand, \
    RemoveShapeCommand, MoveShapeCommand
from app.utils import Singleton, Point


class Brush(metaclass=Singleton):
    def mouse_move(self, controller, x: int, y: int, button):
        raise NotImplementedError

    def mouse_press(self, controller, x: int, y: int, button):
        raise NotImplementedError


class ShapeBrush(Brush):
    def __init__(self):
        super().__init__()
        self._start = None
        self._shape_command_class = None
        self.color = (0, 0, 0)

    def mouse_move(self, controller, x: int, y: int, button):
        if self._shape_command_class is None:
            raise AttributeError(f'Can not draw with instance of {self.__class__}, there is no shape to draw!')

        if self._start is not None:
            shape_command = self._shape_command_class(
                receiver=controller,
                start_x=self._start[0], start_y=self._start[1],
                end_x=x, end_y=y,
                color=(*self.color, 200)      # Adding alpha layer so the preview is semi-transparent
            )
            controller.preview_shape(shape_command.shape)

    def mouse_press(self, controller, x: int, y: int, button):
        if self._shape_command_class is None:
            raise AttributeError(f'Can not draw with instance of {self.__class__}, there is no shape to draw!')

        if self._start is None:
            self._start = (x, y)
        else:
            shape_command = self._shape_command_class(
                receiver=controller,
                start_x=self._start[0], start_y=self._start[1],
                end_x=x, end_y=y,
                color=self.color
            )
            controller.end_preview()
            controller.execute_command(shape_command)
            self._start = None


class DotShapeBrush(ShapeBrush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintDotCommand

    # def _point_distance(self, p1, p2):
    #     return math.floor(
    #         math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    #     )
    #
    # def _lerp(self, v0, v1, i):
    #     return v0 + i * (v1 - v0)
    #
    # def _get_equidistant_points(self, p1, p2):
    #     n = self._point_distance(p1, p2)
    #     return [(self._lerp(p1[0], p2[0], 1./n*i), self._lerp(p1[1], p2[1], 1./n*i)) for i in range(n+1)]

    def _dot_command(self, controller, x: int, y: int):
        shape_command = self._shape_command_class(controller, x, y, self.color)
        controller.execute_command(shape_command)

    def mouse_move(self, controller, x: int, y: int, button):
        if button == Qt.LeftButton:
            self._dot_command(controller, x, y)

    def mouse_press(self, controller, x: int, y: int, button):
        self._dot_command(controller, x, y)

    # def mouse_move(self, controller, x: int, y: int):
    #     if self._start:
    #         for point in self._get_equidistant_points(self._start, (x, y)):
    #             self._dot_command(controller, point[0], point[1])
    #     self._dot_command(controller, x, y)
    #     self._start = (x, y)
    #
    # def mouse_press(self, controller, x: int, y: int):
    #     self._dot_command(controller, x, y)
    #     self._start = None

    def __str__(self):
        return 'Dot'


class LineShapeBrush(ShapeBrush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintLineCommand

    def __str__(self):
        return 'Line'


class PolylineShapeBrush(ShapeBrush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintPolylineCommand
        self._points = []

    def mouse_move(self, controller, x: int, y: int, button):
        if len(self._points) > 0:
            shape_command = self._shape_command_class(
                receiver=controller,
                points=[
                    *self._points,
                    (x, y)
                ],
                color=(*self.color, 200)      # Adding alpha layer so the preview is semi-transparent
            )
            controller.preview_shape(shape_command.shape)

    def mouse_press(self, controller, x: int, y: int, button):
        self._points.append((x, y))
        if button == Qt.RightButton and len(self._points) > 1:
            shape_command = self._shape_command_class(
                receiver=controller,
                points=self._points,
                color=self.color
            )
            controller.end_preview()
            controller.execute_command(shape_command)
            self._points = []

    def __str__(self):
        return 'Polyline'


class RectShapeBrush(ShapeBrush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintRectCommand

    def __str__(self):
        return 'Rectangle'


class CircleShapeBrush(ShapeBrush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintCircleCommand

    def __str__(self):
        return 'Circle'


class MoveShapeBrush(Brush):
    def __init__(self):
        super().__init__()
        self._start = None

    def mouse_move(self, controller, x: int, y: int, button):
        pass

    def mouse_press(self, controller, x: int, y: int, button):
        if self._start is None:
            self._start = (x, y)
        else:
            command = MoveShapeCommand(
                controller,
                start_x=self._start[0], start_y=self._start[1],
                end_x=x, end_y=y
            )
            controller.end_preview()
            controller.execute_command(command)
            self._start = None

    def __str__(self):
        return 'Move'


class RemoveShapeBrush(Brush):
    def mouse_move(self, controller, x: int, y: int, button):
        pass

    def mouse_press(self, controller, x: int, y: int, button):
        command = RemoveShapeCommand(controller, x, y)
        controller.execute_command(command)

    def __str__(self):
        return 'Remove'
