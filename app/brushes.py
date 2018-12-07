from typing import List

from app.commands import Command, PrintLineCommand, PrintRectCommand, PrintCircleCommand, PrintDotCommand
from app.utils import Point


class Brush:
    @staticmethod
    def shape(controller, start_x: int, start_y: int, end_x: int, end_y: int) -> Command:
        raise NotImplementedError


class DotBrush(Brush):
    @staticmethod
    def shape(controller, start_x: int, start_y: int, end_x: int, end_y: int) -> Command:
        return PrintDotCommand(controller, start_x, start_y, (0, 0, 0))


class LineBrush(Brush):
    @staticmethod
    def shape(controller, start_x: int, start_y: int, end_x: int, end_y: int) -> Command:
        return PrintLineCommand(controller, start_x, start_y, end_x, end_y, (255, 255, 255))


class PolylineBrush(Brush):
    @staticmethod
    def shape(controller, start_x: int, start_y: int, end_x: int, end_y: int) -> Command:
        return PrintLineCommand(controller, start_x, start_y, end_x, end_y, (255, 255, 255))


class RectBrush(Brush):
    @staticmethod
    def shape(controller, start_x: int, start_y: int, end_x: int, end_y: int) -> Command:
        return PrintRectCommand(controller, start_x, start_y, end_x, end_y, (255, 255, 255))


class CircleBrush(Brush):
    @staticmethod
    def shape(controller, start_x: int, start_y: int, end_x: int, end_y: int) -> Command:
        return PrintCircleCommand(controller, start_x, start_y, end_x, end_y, (255, 255, 255))
