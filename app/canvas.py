from typing import Tuple

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent

from app.brushes import Brush, MoveShapeBrush, RemoveShapeBrush


class Canvas(QtWidgets.QWidget):
    """
    A (GUI) drawing place for all the shapes. It represents an observer in the observer design pattern.
    """

    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self.brush = MoveShapeBrush()
        self.color = (255, 255, 255)

    def set_brush(self, brush: Brush = MoveShapeBrush()):
        self.brush = brush
        self.brush.color = self.color
        self.setMouseTracking(brush != RemoveShapeBrush())

    def set_color(self, color: Tuple[int, int, int]):
        self.color = color
        self.brush.color = color

    # -------------------------- QWidget overridden methods ----------------------------

    # Overriding paintEvent method of QWidget to respond to QEvent.Paint.
    # This method should be the only place from where we draw with QPainter. This means, that the print_* methods
    # should never be called before executing this method!
    def paintEvent(self, event: QEvent.Paint):
        self._controller.print_all_shapes()

    # By default this event is emitted only when some mouse button is pressed and the mouse moves
    def mouseMoveEvent(self, event: QEvent.MouseMove):
        self.brush.mouse_move(self._controller, event.x(), event.y(), event.buttons())

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        self.brush.mouse_press(self._controller, event.x(), event.y(), event.buttons())
