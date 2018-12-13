from PyQt5 import QtWidgets

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

        # Menu buttons
        self._ui.actionNew.triggered.connect(
            lambda: self._handle_new_action()
        )
        self._ui.actionUndo.triggered.connect(
            lambda: self._handle_undo()
        )
        self._ui.actionRedo.triggered.connect(
            lambda: self._handle_redo()
        )
        self.disable_undo()
        self.disable_redo()

        # Setting specific brush for canvas after clicking on one of the tool buttons
        self._ui.dotButton.clicked.connect(
            lambda: self.canvas.set_brush(DotBrush())
        )
        self._ui.polylineButton.clicked.connect(
            lambda: self.canvas.set_brush(PolylineBrush())
        )
        self._ui.lineButton.clicked.connect(
            lambda: self.canvas.set_brush(LineBrush())
        )
        self._ui.rectagleButton.clicked.connect(
            lambda: self.canvas.set_brush(RectBrush())
        )
        self._ui.circleButton.clicked.connect(
            lambda: self.canvas.set_brush(CircleBrush())
        )

        self._ui.canvasHolder.setWidget(self.canvas)

    def _handle_new_action(self):
        self._controller.restart()

    def _handle_undo(self):
        self._controller.undo()

    def _handle_redo(self):
        self._controller.redo()

    def enable_undo(self):
        self._ui.actionUndo.setEnabled(True)

    def disable_undo(self):
        self._ui.actionUndo.setEnabled(False)

    def enable_redo(self):
        self._ui.actionRedo.setEnabled(True)

    def disable_redo(self):
        self._ui.actionRedo.setEnabled(False)
