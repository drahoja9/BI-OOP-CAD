from typing import Tuple

from app.shapes import Shape, Rectangle, Circle
from app.utils import Point, Color, distance


class ShapeFactory:
    @staticmethod
    def get_shape(start_x: int, start_y: int, color: Tuple[int, int, int], **kwargs) -> Shape:
        raise NotImplementedError


# --------------- Rectangle ---------------


class DimensionsRectFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_x: int, start_y: int, color: Tuple[int, int, int], **kwargs) -> Rectangle:
        width = kwargs['width']
        height = kwargs['height']

        rectangle = Rectangle(
            Point(start_x, start_y),
            width,
            height,
            Color(*color)
        )
        return rectangle


class PointsRectFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_x: int, start_y: int, color: Tuple[int, int, int], **kwargs) -> Rectangle:
        end_x = kwargs['end_x']
        end_y = kwargs['end_y']

        width = abs(start_x - end_x)
        height = abs(start_y - end_y)
        rectangle = Rectangle(
            Point(min(start_x, end_x), min(start_y, end_y)),
            width,
            height,
            Color(*color)
        )
        return rectangle

# --------------- Circle ---------------


class DimensionsCircleFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_x: int, start_y: int, color: Tuple[int, int, int], **kwargs) -> Circle:
        radius = kwargs['radius']

        center = (start_x, start_y)
        circle = Circle(
            Point(*center),
            int(radius),
            Color(*color)
        )
        return circle


class PointsCircleFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_x: int, start_y: int, color: Tuple[int, int, int], **kwargs) -> Circle:
        end_x = kwargs['end_x']
        end_y = kwargs['end_y']

        center = (start_x, start_y)
        radius = distance(Point(*center), Point(end_x, end_y))
        circle = Circle(
            Point(*center),
            int(radius),
            Color(*color)
        )
        return circle
