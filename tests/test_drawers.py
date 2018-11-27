import pytest

from PyQt5.QtGui import QColor

from app.shapes import Shape, Dot, Line, Rectangle, Circle
from app.utils import Point
from app.drawers import Drawer


def test_abstract_drawer():
    empty_drawer = Drawer(None)
    assert empty_drawer.shapes == []

    empty_drawer.add_shape(Dot(Point(10, 10), QColor('steelblue')))
    empty_drawer.add_shapes(
        Rectangle(Point(0, 200), 240, 167, QColor(100, 0, 100)),
        Circle(Point(49, 70), 15, QColor(250, 250, 250))
    )
    assert empty_drawer.shapes == [
        Dot(Point(10, 10), QColor('steelblue')),
        Rectangle(Point(0, 200), 240, 167, QColor(100, 0, 100)),
        Circle(Point(49, 70), 15, QColor(250, 250, 250))
    ]

    drawer = Drawer([
        Dot(Point(10, 10), QColor('steelblue')),
        Rectangle(Point(0, 200), 240, 167, QColor(100, 0, 100)),
        Circle(Point(49, 70), 15, QColor(250, 250, 250))
    ])
    assert empty_drawer == drawer

    drawer.remove_last_shape()
    assert drawer.shapes == [
        Dot(Point(10, 10), QColor('steelblue')),
        Rectangle(Point(0, 200), 240, 167, QColor(100, 0, 100))
    ]

    empty_drawer.remove_shape(Dot(Point(10, 10), QColor('steelblue')))
    assert empty_drawer.shapes == [
        Rectangle(Point(0, 200), 240, 167, QColor(100, 0, 100)),
        Circle(Point(49, 70), 15, QColor(250, 250, 250))
    ]

    assert empty_drawer != drawer

    with pytest.raises(NotImplementedError):
        empty_drawer.draw_dot(None)

    with pytest.raises(NotImplementedError):
        empty_drawer.draw_line(None)

    with pytest.raises(NotImplementedError):
        empty_drawer.draw_rectangle(None)

    with pytest.raises(NotImplementedError):
        empty_drawer.draw_circle(None)
