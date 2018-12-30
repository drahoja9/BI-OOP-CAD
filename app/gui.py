import getpass

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog, QFileDialog

from app.ui.main_window import Ui_MainWindow
from app.canvas import Canvas
from app.brushes import LineShapeBrush, RectShapeBrush, CircleShapeBrush, DotShapeBrush, PolylineShapeBrush, \
    RemoveShapeBrush, Brush


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
            lambda: self._controller.restart()
        )
        self._ui.actionSave.triggered.connect(
            lambda: self._handle_file_save()
        )
        self._ui.actionUndo.triggered.connect(
            lambda: self._controller.undo()
        )
        self._ui.actionRedo.triggered.connect(
            lambda: self._controller.redo()
        )
        self.disable_undo()
        self.disable_redo()

        # Setting specific brush for canvas after clicking on one of the tool buttons
        self._ui.dotButton.clicked.connect(
            lambda: self._toggle_brush(DotShapeBrush())
        )
        self._ui.polylineButton.clicked.connect(
            lambda: self._toggle_brush(PolylineShapeBrush())
        )
        self._ui.lineButton.clicked.connect(
            lambda: self._toggle_brush(LineShapeBrush())
        )
        self._ui.rectagleButton.clicked.connect(
            lambda: self._toggle_brush(RectShapeBrush())
        )
        self._ui.circleButton.clicked.connect(
            lambda: self._toggle_brush(CircleShapeBrush())
        )
        self._ui.removeButton.clicked.connect(
            lambda: self._toggle_brush(RemoveShapeBrush())
        )
        self._ui.colorButton.clicked.connect(
            lambda: self._handle_color_pick()
        )

        self._ui.manualInput.returnPressed.connect(
            lambda: self._manual_input_pressed()
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

    def _handle_color_pick(self):
        # Color picker will popup and returns chosen color
        color = QColorDialog().getColor(QColor(*self.canvas.color))
        if color.isValid():
            self._ui.colorButton.setStyleSheet(f'background-color: {color.name()}')
            r, g, b, alpha = color.getRgb()
            self.canvas.set_color((r, g, b))

    def _handle_file_save(self):
        # Save file dialog will open and returns tuple (name of the saved file, type)
        user = getpass.getuser()
        name = QFileDialog().getSaveFileName(self, 'Save File', f'/home/{user}/untitled.txt')
        self._controller.save(name[0])

    def _manual_input_pressed(self):
        command = self._ui.manualInput.text()
        self._ui.manualInput.setText('')
        print(command)

    def enable_undo(self):
        self._ui.actionUndo.setEnabled(True)

    def disable_undo(self):
        self._ui.actionUndo.setEnabled(False)

    def enable_redo(self):
        self._ui.actionRedo.setEnabled(True)

    def disable_redo(self):
        self._ui.actionRedo.setEnabled(False)

    def print_newline_to_history(self, line: str):
        history = self._ui.history.text()
        self._ui.history.setText(history + line + '\n')

    def delete_from_history(self, number_of_lines: int = 1):
        history = self._ui.history.text()
        # Subtracting 1 from `number of lines` as the last line is always empty (there's always `\n` at the end)
        history = history.split('\n')[:(-number_of_lines - 1)]
        history = '\n'.join(history)
        if history:
            history += '\n'
        self._ui.history.setText(history)
