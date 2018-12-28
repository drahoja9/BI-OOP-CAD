from typing import Tuple

from app.shapes import Shape, Rectangle, Circle
from app.utils import Point, Color, distance


class ShapeFactory:
    @staticmethod
    def get_shape(start_point_x: int, start_point_y: int, color: Tuple[int, int, int], **kwargs) -> Shape:
        raise NotImplementedError


# --------------- Rectangle ---------------


class DimensionsRectFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_point_x: int, start_point_y: int, color: Tuple[int, int, int], **kwargs) -> Rectangle:
        width = kwargs['width']
        height = kwargs['height']

        rectangle = Rectangle(
            Point(start_point_x, start_point_y),
            width,
            height,
            Color(*color)
        )
        return rectangle


class PointsRectFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_point_x: int, start_point_y: int, color: Tuple[int, int, int], **kwargs) -> Rectangle:
        end_point_x = kwargs['end_point_x']
        end_point_y = kwargs['end_point_y']

        width = abs(start_point_x - end_point_x)
        height = abs(start_point_y - end_point_y)
        rectangle = Rectangle(
            Point(min(start_point_x, end_point_x), min(start_point_y, end_point_y)),
            width,
            height,
            Color(*color)
        )
        return rectangle

# --------------- Circle ---------------


class DimensionsCircleFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_point_x: int, start_point_y: int, color: Tuple[int, int, int], **kwargs) -> Circle:
        radius = kwargs['radius']

        center = (start_point_x, start_point_y)
        circle = Circle(
            Point(*center),
            int(radius),
            Color(*color)
        )
        return circle


class PointsCircleFactory(ShapeFactory):
    @staticmethod
    def get_shape(start_point_x: int, start_point_y: int, color: Tuple[int, int, int], **kwargs) -> Circle:
        end_point_x = kwargs['end_point_x']
        end_point_y = kwargs['end_point_y']

        center = (start_point_x, start_point_y)
        radius = distance(Point(*center), Point(end_point_x, end_point_y))
        circle = Circle(
            Point(*center),
            int(radius),
            Color(*color)
        )
        return circle
