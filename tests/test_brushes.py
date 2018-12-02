import pytest

from app.brushes import Brush, DotBrush, LineBrush, RectBrush, CircleBrush
from app.commands import PrintDotCommand, PrintLineCommand, PrintRectCommand, PrintCircleCommand


def test_abstract_brush():
    with pytest.raises(NotImplementedError):
        Brush.shape(None, 0, 0, 0, 0)


def test_dot_brush():
    assert DotBrush.shape(None, 1, 2, 3, 4) == PrintDotCommand(None, 1, 2, (0, 0, 0))


def test_line_brush():
    assert LineBrush.shape(None, 1, 2, 3, 4) == PrintLineCommand(None, 1, 2, 3, 4, (255, 255, 255))


def test_rect_brush():
    assert RectBrush.shape(None, 1, 2, 3, 4) == PrintRectCommand(None, 1, 2, 3, 4, (255, 255, 255))


def test_circle_brush():
    assert CircleBrush.shape(None, 1, 2, 3, 4) == PrintCircleCommand(None, 1, 2, 3, 4, (255, 255, 255))
