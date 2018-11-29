from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent


class Canvas(QtWidgets.QWidget):
    """
    A (GUI) drawing place for all the shapes. It represents observer in observer design pattern.
    """
    def __init__(self, controller):
        super().__init__()
        self._controller = controller

    # -------------------------- QWidget overridden methods ----------------------------

    # Overriding paintEvent method of QWidget to respond to QEvent.Paint.
    # This method should be the only place from where we draw with QPainter. This means, that the print_* methods
    # should never be called before executing this method!
    def paintEvent(self, event: QEvent.Paint):
        self._controller.print_all_shapes()

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        ...
