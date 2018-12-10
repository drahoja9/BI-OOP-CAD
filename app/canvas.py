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
