import math
from typing import Type

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent

from app.brushes import Brush


class Canvas(QtWidgets.QWidget):
    """
    A (GUI) drawing place for all the shapes. It represents an observer in the observer design pattern.
    """

    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self._brush = None

    def set_brush(self, brush: Brush):
        if self._brush != brush:
            self._brush = brush
        else:
            self._brush = None

    def _add_command(self, start_x: int, start_y: int, end_x: int, end_y: int):
        shape_command = self._brush.shape(
            self._controller,
            start_x,
            start_y,
            end_x,
            end_y
        )
        self._controller.execute_command(shape_command)

    def _complete_command(self, start_x: int, start_y: int, end_x: int, end_y: int):
        self._add_command(start_x, start_y, end_x, end_y)
        self._start = None

    def _pointDistance(self, p1, p2):
        return math.floor(
            math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))

    def _lerp(self, v0, v1, i):
        return v0 + i * (v1 - v0)

    def _getEquidistantPoints(self, p1, p2):
        n = self._pointDistance(p1, p2)
        return [(self._lerp(p1[0], p2[0], 1./n*i), self._lerp(p1[1], p2[1], 1./n*i)) for i in range(n+1)]

    # -------------------------- QWidget overridden methods ----------------------------

    # Overriding paintEvent method of QWidget to respond to QEvent.Paint.
    # This method should be the only place from where we draw with QPainter. This means, that the print_* methods
    # should never be called before executing this method!
    def paintEvent(self, event: QEvent.Paint):
        self._controller.print_all_shapes()

    # By default this event is emitted only when some mouse button is pressed and the mouse moves
    def mouseMoveEvent(self, event: QEvent.MouseMove):
        if self._brush is not None:
            self._brush.mouse_move(self._controller, event.x(), event.y())

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        if self._brush is not None:
            self._brush.mouse_press(self._controller, event.x(), event.y())
