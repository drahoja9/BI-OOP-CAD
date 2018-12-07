import math
from typing import Type

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, Qt

from app.brushes import Brush, DotBrush, PolylineBrush
from app.utils import Point


class Canvas(QtWidgets.QWidget):
    """
    A (GUI) drawing place for all the shapes. It represents an observer in the observer design pattern.
    """

    def __init__(self, controller):
        super().__init__()
        self._controller = controller

        self._start = None
        self._brush = None

        # Used for pen
        self._last = None

    def set_brush(self, brush: Type[Brush]):
        if self._brush != brush:
            self._brush = brush
        else:
            self._brush = None
        self._start = None

    def _addCommand(self, start_x: int, start_y: int, end_x: int, end_y: int):
        shape_command = self._brush.shape(
            self._controller,
            start_x,
            start_y,
            end_x,
            end_y
        )
        self._controller.execute_command(shape_command)

    def _completeCommand(self, start_x: int, start_y: int, end_x: int, end_y: int):
        self._addCommand(start_x, start_y, end_x, end_y)
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

    def mouseMoveEvent(self, event: QEvent.MouseMove):
        if self._brush == DotBrush:
            if (self._last):
                for point in self._getEquidistantPoints(self._last, (event.x(), event.y())):
                    self._addCommand(point[0], point[1], 0, 0)
            self._addCommand(event.x(), event.y(), 0, 0)
            self._last = (event.x(), event.y())

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        self._last = None

        if self._brush:
            # Init everything
            if self._start is None:
                self._start = (event.x(), event.y())

                # Dot
                if self._brush == DotBrush:
                    self._completeCommand(
                        self._start[0], self._start[1], event.x(), event.y())
            else:
                # Polyline
                if self._brush == PolylineBrush:
                    # End of polyline
                    if event.button() == Qt.RightButton:
                        self._start = None
                        return

                    self._addCommand(
                        self._start[0], self._start[1], event.x(), event.y())
                    self._start = (event.x(), event.y())

                # Draw other
                else:
                    self._completeCommand(
                        self._start[0], self._start[1], event.x(), event.y())
