from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QColor

from app.ui.main_window import Ui_MainWindow
from app.canvas import Canvas
from app.brushes import LineBrush, RectBrush, CircleBrush, DotBrush, PolylineBrush


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller

        # Initializing the whole UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.canvas = Canvas(controller)
        self.color = QColor(0, 0, 0)

        # Menu buttons
        self._ui.actionNew.triggered.connect(
            lambda: self._handle_new_action()
        )

        self._ui.colorButton.clicked.connect(
            lambda: self._hadne_color_pick()
        )

        # Setting specific brush for canvas after clicking on one of the tool buttons
        self._ui.dotButton.clicked.connect(
            lambda: self.canvas.set_brush(DotBrush(self.color))
        )
        self._ui.polylineButton.clicked.connect(
            lambda: self.canvas.set_brush(PolylineBrush(self.color))
        )
        self._ui.lineButton.clicked.connect(
            lambda: self.canvas.set_brush(LineBrush(self.color))
        )
        self._ui.rectagleButton.clicked.connect(
            lambda: self.canvas.set_brush(RectBrush(self.color))
        )
        self._ui.circleButton.clicked.connect(
            lambda: self.canvas.set_brush(CircleBrush(self.color))
        )

        self._ui.canvasHolder.setWidget(self.canvas)

    def _hadne_color_pick(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            self._ui.colorButton.setStyleSheet(f"background-color: {self.color.name()}")
            # this should update brush, but it ain't workin for some reason
            brushClass = self.canvas.get_brush().__class__
            if brushClass is not None:
                self.canvas.set_brush(brushClass(self.color))

    def _handle_new_action(self):
        self._controller.restart()
