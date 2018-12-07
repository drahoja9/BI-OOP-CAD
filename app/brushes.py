from app.commands import PrintLineCommand, PrintRectCommand, PrintCircleCommand, PrintDotCommand
from app.utils import Singleton


class Brush(metaclass=Singleton):
    def __init__(self):
        self._start = None
        self._shape_command_class = None

    def mouse_move(self, controller, x: int, y: int):
        pass

    def mouse_press(self, controller, x: int, y: int):
        if self._start is None:
            self._start = (x, y)
        else:
            shape_command = self._shape_command_class(
                controller,
                self._start[0],
                self._start[1],
                x,
                y,
                (255, 255, 255)
            )
            controller.execute_command(shape_command)
            self._start = None


class DotBrush(Brush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintDotCommand

    def _dot_command(self, controller, x: int, y: int):
        shape_command = self._shape_command_class(controller, x, y, (0, 0, 0))
        controller.execute_command(shape_command)

    def mouse_move(self, controller, x: int, y: int):
        self._dot_command(controller, x, y)

    def mouse_press(self, controller, x: int, y: int):
        self._dot_command(controller, x, y)


class LineBrush(Brush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintLineCommand


# class PolylineBrush(Brush):
#     @classmethod
#     def paint(cls, controller, x: int, y: int):
#         if cls._start is None:
#             cls._start = (x, y)
#         else:
#             shape_command = PrintLineCommand(
#                 controller,
#                 cls._start[0],
#                 cls._start[0],
#                 x,
#                 y,
#                 (255, 255, 255)
#             )
#             controller.execute_command(shape_command)
#
#     @staticmethod
#     def shape(controller, start_x: int, start_y: int, end_x: int, end_y: int) -> Command:
#         return PrintLineCommand(controller, start_x, start_y, end_x, end_y, (255, 255, 255))


class RectBrush(Brush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintRectCommand


class CircleBrush(Brush):
    def __init__(self):
        super().__init__()
        self._shape_command_class = PrintCircleCommand
