from typing import Dict

import pytest

from app.shapes import Dot, Line, Rectangle, Circle, Shape, Polyline
from app.utils import Point, Color


@pytest.fixture
def shapes() -> Dict[str, Shape]:
    return {
        'dot': Dot(Point(10, 200000000), Color(1, 2, 3)),
        'line': Line(Point(1000, -1000), Point(0, -1000), Color(0, 0, 0)),
        'polyline': Polyline(Point(10, 10), Point(20, 20), Point(30, 10), color=Color(48, 210, 111)),
        'rectangle': Rectangle(Point(0, 0), 1, 50000, Color(255, 255, 255)),
        'circle': Circle(Point(12345, 54321), 999, Color(123, 255, 0))
    }
