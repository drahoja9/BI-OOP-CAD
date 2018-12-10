from app.utils import Point, Singleton


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
