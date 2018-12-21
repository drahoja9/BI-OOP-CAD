from PyQt5 import QtWidgets

from app.ui.main_window import Ui_MainWindow
from app.canvas import Canvas
from app.brushes import LineBrush, RectBrush, CircleBrush, DotBrush, PolylineBrush, Brush


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller

        # Initializing the whole UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._set_status()

        self.canvas = Canvas(controller)

        # Menu buttons
        self._ui.actionNew.triggered.connect(
            lambda: self._handle_new_action()
        )

        # Setting specific brush for canvas after clicking on one of the tool buttons
        self._ui.dotButton.clicked.connect(
            lambda: self._toggle_brush(DotBrush())
        )
        self._ui.polylineButton.clicked.connect(
            lambda: self._toggle_brush(PolylineBrush())
        )
        self._ui.lineButton.clicked.connect(
            lambda: self._toggle_brush(LineBrush())
        )
        self._ui.rectagleButton.clicked.connect(
            lambda: self._toggle_brush(RectBrush())
        )
        self._ui.circleButton.clicked.connect(
            lambda: self._toggle_brush(CircleBrush())
        )

        self._ui.canvasHolder.setWidget(self.canvas)

    def _handle_new_action(self):
        self._controller.restart()

    def _set_status(self, message: str = 'No tool'):
        self.statusBar().showMessage(message)

    def _toggle_brush(self, brush: Brush):
        if self.canvas.brush != brush:
            self.canvas.set_brush(brush)
            self._set_status(str(brush))
        else:
            self.canvas.set_brush()
            self._set_status()
