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
