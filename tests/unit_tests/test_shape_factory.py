import pytest

from app.shapes import Rectangle, Circle
from app.utils import Point, Color
from app.shape_factory import ShapeFactory, PointsRectFactory, DimensionsRectFactory, \
    PointsCircleFactory, DimensionsCircleFactory


def test_abstract_shape_factory():
    with pytest.raises(NotImplementedError):
        ShapeFactory.get_shape(1, 2, (3, 4, 5))


# --------------- Rectangle factories tests ---------------


def test_points_rect_factory():
    rectangle = PointsRectFactory.get_shape(0, 0, (0, 20, 40), end_x=10, end_y=20)
    assert rectangle == Rectangle(Point(0, 0), 10, 20, Color(0, 20, 40))


def test_dimensions_rect_factory():
    rectangle = DimensionsRectFactory.get_shape(0, 0, (0, 20, 40), width=10, height=20)
    assert rectangle == Rectangle(Point(0, 0), 10, 20, Color(0, 20, 40))


def test_rect_factories_equal():
    points_rectangle = PointsRectFactory.get_shape(0, 0, (0, 20, 40), end_x=10,end_y=20)
    dimensions_rectangle = DimensionsRectFactory.get_shape(0, 0, (0, 20, 40), width=10, height=20)
    assert points_rectangle == dimensions_rectangle


# --------------- Circle factories tests ---------------


def test_points_circle_factory():
    circle = PointsCircleFactory.get_shape(0, 0, (0, 20, 40), end_x=100, end_y=100)
    assert circle == Circle(Point(0, 0), 141, Color(0, 20, 40))


def test_dimensions_circle_factory():
    circle = DimensionsCircleFactory.get_shape(0, 0, (0, 20, 40), radius=141)
    assert circle == Circle(Point(0, 0), 141, Color(0, 20, 40))


def test_circle_factories_equal():
    points_circle = PointsCircleFactory.get_shape(0, 0, (0, 20, 40), end_x=100, end_y=100)
    dimensions_circle = DimensionsCircleFactory.get_shape(0, 0, (0, 20, 40), radius=141)
    assert points_circle == dimensions_circle
