from typing import Type

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent

from app.brushes import Brush, DotBrush


class Canvas(QtWidgets.QWidget):
    """
    A (GUI) drawing place for all the shapes. It represents an observer in the observer design pattern.
    """

    def __init__(self, controller):
        super().__init__()
        self._controller = controller

        self._start = None
        self._brush = None

    def set_brush(self, brush: Type[Brush]):
        if self._brush != brush:
            self._brush = brush
        else:
            self._brush = None
        self._start = None

    # -------------------------- QWidget overridden methods ----------------------------

    # Overriding paintEvent method of QWidget to respond to QEvent.Paint.
    # This method should be the only place from where we draw with QPainter. This means, that the print_* methods
    # should never be called before executing this method!
    def paintEvent(self, event: QEvent.Paint):
        self._controller.print_all_shapes()

    def mouseMoveEvent(self, event: QEvent.MouseMove):
        if self._brush == DotBrush:
            dot_command = self._brush.shape(self._controller, event.x(), event.y(), 0, 0)
            self._controller.execute_command(dot_command)

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        if self._brush:
            if self._start is None:
                self._start = (event.x(), event.y())
            else:
                shape_command = self._brush.shape(
                    self._controller,
                    self._start[0],
                    self._start[1],
                    event.x(),
                    event.y()
                )
                self._controller.execute_command(shape_command)
                self._start = None
