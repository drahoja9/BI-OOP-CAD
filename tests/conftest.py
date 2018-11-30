from typing import Dict

import pytest
from PyQt5.QtGui import QColor

from app.shapes import Dot, Line, Rectangle, Circle, Shape
from app.utils import Point


@pytest.fixture(scope="session")
def shapes() -> Dict[str, Shape]:
    return {
        'dot': Dot(Point(10, 200000000), QColor(1, 2, 3)),
        'line': Line(Point(1000, -1000), Point(-123, 321), QColor(0, 0, 0)),
        'rectangle': Rectangle(Point(0, 0), 1, 50000, QColor(255, 255, 255)),
        'circle': Circle(Point(12345, 54321), 999, QColor(123, 255, 0))
    }
