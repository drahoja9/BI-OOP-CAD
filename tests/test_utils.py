import math

import pytest

from app.utils import Point, Singleton, Color, distance


class TestSingletonClass(metaclass=Singleton):
    a = 1

    def __init__(self):
        self.b = 20


def test_point():
    p1 = Point(123, 321)
    assert p1.x == 123
    assert p1.y == 321

    p2 = Point(-40, 0)
    assert p2.x == -40
    assert p2.y == 0

    p3 = Point(321, 123)
    p4 = Point(123, 321)
    assert p3 != p4
    assert p1 == p1
    assert p1 == p4

    assert p1.__repr__() == '[123, 321]'
    assert str(p2) == '[-40, 0]'

    assert p1 + p2 == Point(83, 321)
    assert p4 + p3 + p2 + p1 == Point(527, 765)
    assert p1 - p2 == Point(163, 321)
    assert p4 - p3 - p2 - p1 == Point(-281, -123)

    p4 += p3
    assert p4 == Point(444, 444)

    p4 -= p2
    assert p4 == Point(484, 444)


def test_color():
    c1 = Color(255, 123, 0)
    c2 = Color(255, 123, 0, 255)
    c3 = Color(123, 255, 0)

    assert c1.r == 255
    assert c1.g == 123
    assert c1.b == 0
    assert c1.alpha == 255

    def unpacking(r, g, b, alpha):
        assert r == 255
        assert g == 123
        assert b == 0
        assert alpha == 255

    unpacking(*c1)
    unpacking(*c2)

    assert c1 == c2
    assert c1 != c3
    assert c2 != c3

    assert str(c1) == str(c2) == 'Color(255, 123, 0, alpha=255)'
    assert str(c3) == 'Color(123, 255, 0, alpha=255)'

    with pytest.raises(ValueError):
        c4 = Color(255, 255, 256)

    with pytest.raises(ValueError):
        c5 = Color(0, -1, 0)

    with pytest.raises(ValueError):
        c6 = Color(255, 255, 255, 256)


def test_singleton():
    a = TestSingletonClass()
    b = TestSingletonClass()
    c = TestSingletonClass()
    assert a == b == c

    a.a = 2
    assert a.a == b.a == c.a == 2
    b.b = 123
    assert a.b == b.b == c.b == 123

    assert a == b == c


def test_distance():
    assert distance(Point(0, 0), Point(0, 0)) == 0
    assert distance(Point(0, 0), Point(10, 0)) == 10
    assert distance(Point(0, 0), Point(0, -100)) == 100
    assert math.isclose(distance(Point(0, 0), Point(20, 20)), 28.284271247461902) is True
