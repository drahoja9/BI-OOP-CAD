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
        self._is_tracking_mouse = False

    def set_brush(self, brush: Brush):
        self._toggle_mouse_tracking(False)
        if self._brush != brush:
            self._brush = brush
        else:
            self._brush = None

    def _toggle_mouse_tracking(self, state: bool = None):
        # Tracking the mouse movement even without any mouse button pressed down
        # in order to enable preview of drawn shape
        self._is_tracking_mouse = state if state is not None else not self._is_tracking_mouse
        self.setMouseTracking(self._is_tracking_mouse)

    # -------------------------- QWidget overridden methods ----------------------------

    # Overriding paintEvent method of QWidget to respond to QEvent.Paint.
    # This method should be the only place from where we draw with QPainter. This means, that the print_* methods
    # should never be called before executing this method!
    def paintEvent(self, event: QEvent.Paint):
        self._controller.print_all_shapes()

    # By default this event is emitted only when some mouse button is pressed and the mouse moves
    def mouseMoveEvent(self, event: QEvent.MouseMove):
        if self._brush is not None:
            self._brush.mouse_move(self._controller, event.x(), event.y(), event.buttons())

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        if self._brush is not None:
            self._toggle_mouse_tracking()
            self._brush.mouse_press(self._controller, event.x(), event.y())
