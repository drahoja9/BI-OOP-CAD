import math
from typing import Iterator


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f'[{self.x}, {self.y}]'


class Color:
    def __init__(self, r: int, g: int, b: int, alpha: int = 255):
        if r > 255 or r < 0 or g > 255 or g < 0 or b > 255 or b < 0 or alpha < 0 or alpha > 255:
            raise ValueError('Each color from RGBa must be from [0, 255] interval!')
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

    def __iter__(self) -> Iterator[int]:
        return iter([self.r, self.g, self.b, self.alpha])

    def __eq__(self, other) -> bool:
        return self.r == other.r and self.g == other.g and self.b == other.b and self.alpha == other.alpha

    def __repr__(self) -> str:
        return f'Color({self.r}, {self.g}, {self.b}, alpha={self.alpha})'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            # Calling __init__ of given class even though we return the same instance
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


def distance(a: Point, b: Point):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
