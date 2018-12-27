from typing import List

import pytest

from app.commands import Command, PrintDotCommand, PrintLineCommand, PrintRectCommand, PrintCircleCommand, \
    PrintPolylineCommand, RemoveShapeCommand, ListShapeCommand
from app.shapes import Shape, Dot, Line, Rectangle, Circle, Polyline
from app.utils import Point, Color

from app.shape_factories import *

"--------------- Rectangle factories tests ---------------"


def test_points_rect_factory():
    factory = PointsRectFactory(start_point_x=0, start_point_y=0,
                                end_point_x=10, end_point_y=20,
                                color=(0, 20, 40))
    rectangle = factory.get_shape()
    assert rectangle == Rectangle(Point(0, 0), 10, 20, Color(0, 20, 40))


def test_dimensions_rect_factory():
    factory = DimensionsRectFactory(start_point_x=0, start_point_y=0,
                                    width=10, height=20,
                                    color=(0, 20, 40))
    rectangle = factory.get_shape()
    assert rectangle == Rectangle(Point(0, 0), 10, 20, Color(0, 20, 40))


def test_rect_factories_equal():
    points_factory = PointsRectFactory(start_point_x=0, start_point_y=0,
                                       end_point_x=10, end_point_y=20,
                                       color=(0, 20, 40))
    dimensions_factory = DimensionsRectFactory(start_point_x=0, start_point_y=0,
                                               width=10, height=20,
                                               color=(0, 20, 40))
    points_rectangle = points_factory.get_shape()
    dimensions_rectangle = dimensions_factory.get_shape()
    assert points_rectangle == dimensions_rectangle


"--------------- Circle factories tests ---------------"


def test_points_circle_factory():
    factory = PointsCircleFactory(start_point_x=0, start_point_y=0,
                                  end_point_x=100, end_point_y=100,
                                  color=(0, 20, 40))
    rectangle = factory.get_shape()
    assert rectangle == Circle(Point(0, 0), 141, Color(0, 20, 40))


def test_dimensions_circle_factory():
    factory = DimensionsCircleFactory(center_x=0, center_y=0,
                                      radius=141,
                                      color=(0, 20, 40))
    rectangle = factory.get_shape()
    assert rectangle == Circle(Point(0, 0), 141, Color(0, 20, 40))


def test_circle_factories_equal():
    points_factory = PointsCircleFactory(start_point_x=0, start_point_y=0,
                                         end_point_x=100, end_point_y=100,
                                         color=(0, 20, 40))
    dimensions_factory = DimensionsCircleFactory(center_x=0, center_y=0,
                                                 radius=141,
                                                 color=(0, 20, 40))
    points_circle = points_factory.get_shape()
    dimensions_circle = dimensions_factory.get_shape()
    assert points_circle == dimensions_circle
