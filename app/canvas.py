from typing import Tuple

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
        self.color = (0, 0, 0)

    def set_brush(self, brush: Brush):
        if self._brush != brush:
            self._brush = brush
            self._brush.color = self.color
            self.setMouseTracking(True)
        else:
            self._brush = None
            self.setMouseTracking(False)

    def set_color(self, color: Tuple[int, int, int]):
        self.color = color
        if self._brush is not None:
            self._brush.color = color

    # -------------------------- QWidget overridden methods ----------------------------

    # By default this event is emitted only when some mouse button is pressed and the mouse moves
    def mouseMoveEvent(self, event: QEvent.MouseMove):
        if self._brush is not None:
            self._brush.mouse_move(self._controller, event.x(), event.y(), event.buttons())

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        if self._brush is not None:
            self._brush.mouse_press(self._controller, event.x(), event.y(), event.buttons())
