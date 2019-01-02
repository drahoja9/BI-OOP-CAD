import getpass

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtWidgets import QColorDialog, QFileDialog

from app.commands import ClearCommand, SaveCommand, LoadCommand
from app.ui.main_window import Ui_MainWindow
from app.ui.clear_dialog import Ui_clearDialog
from app.canvas import Canvas
from app.brushes import LineShapeBrush, RectShapeBrush, CircleShapeBrush, DotShapeBrush, PolylineShapeBrush, \
    RemoveShapeBrush, Brush, MoveShapeBrush


class ClearDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self._ui = Ui_clearDialog()
        self._ui.setupUi(self)

        self.accepted = None
        self._ui.clearButtonBox.accepted.connect(self._accepted)
        self._ui.clearButtonBox.rejected.connect(self._rejected)

        self.exec_()

    def _accepted(self):
        self.accepted = True

    def _rejected(self):
        self.accepted = False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller

        # Initializing the whole UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.set_status()

        self.canvas = Canvas(controller)

        # Menu buttons
        self._ui.actionNew.triggered.connect(
            lambda: self._handle_action_new()
        )
        self._ui.actionSave.triggered.connect(
            lambda: self.save_dialog()
        )
        self._ui.actionLoad.triggered.connect(
            lambda: self.load_dialog()
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
        self._ui.lineButton.clicked.connect(
            lambda: self._toggle_brush(LineShapeBrush())
        )
        self._ui.polylineButton.clicked.connect(
            lambda: self._toggle_brush(PolylineShapeBrush())
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
        self.brush_buttons = {
            DotShapeBrush(): self._ui.dotButton,
            LineShapeBrush(): self._ui.lineButton,
            PolylineShapeBrush(): self._ui.polylineButton,
            RectShapeBrush(): self._ui.rectagleButton,
            CircleShapeBrush(): self._ui.circleButton,
            RemoveShapeBrush(): self._ui.removeButton
        }

        self._ui.manualInput.returnPressed.connect(
            lambda: self._handle_user_input()
        )

        self._ui.canvasHolder.setWidget(self.canvas)

    # ------------------------------------------------ Handlers -------------------------------------------------------

    def _handle_action_new(self):
        command = ClearCommand(self._controller)
        self._controller.execute_command(command)

    def _handle_save_file(self):
        command = SaveCommand(self._controller)
        self._controller.execute_command(command)

    def _handle_load_file(self):
        command = LoadCommand(self._controller)
        self._controller.execute_command(command)

    def _toggle_brush(self, brush: Brush):
        if self.canvas.brush != MoveShapeBrush():
            # Un-checking the previous brush button
            previous_brush_button = self.brush_buttons[self.canvas.brush]
            previous_brush_button.setChecked(False)

        if self.canvas.brush != brush:
            self.canvas.set_brush(brush)
            self.set_status(str(brush))
        else:
            self.canvas.set_brush()
            self.set_status()

    def _handle_color_pick(self):
        # Color picker will popup and returns chosen color
        color = QColorDialog().getColor(QColor(*self.canvas.color))
        if color.isValid():
            self._ui.colorButton.setStyleSheet(f'background-color: {color.name()}')
            r, g, b, alpha = color.getRgb()
            self.canvas.set_color((r, g, b))

    def _handle_user_input(self):
        command_text = self._ui.manualInput.text()
        self._ui.manualInput.setText('')
        if command_text != '' and not command_text.isspace():
            self._controller.parse_command(command_text)

    # --------------------------------------------- Main window methods -----------------------------------------------

    @staticmethod
    def clear_dialog() -> bool:
        res = ClearDialog()
        return res.accepted

    def set_status(self, message: str = str(MoveShapeBrush())):
        self.statusBar().showMessage(message)

    def save_dialog(self, path_to_file: str = None):
        # Save file dialog will open and returns tuple (name of the saved file, type)
        user = getpass.getuser()
        path = path_to_file or f'/home/{user}/untitled.txt'
        name, _ = QFileDialog().getSaveFileName(self, 'Save File', path)
        if name:
            self._controller.save(name)

    def load_dialog(self, path_to_file: str = None):
        # Load file dialog will open and returns tuple (name of the loaded file, type)
        user = getpass.getuser()
        path = path_to_file or f'/home/{user}/untitled.txt'
        name, _ = QFileDialog().getOpenFileName(self, 'Load File', path)
        if name:
            self._controller.load(name)

    def enable_undo(self):
        self._ui.actionUndo.setEnabled(True)

    def disable_undo(self):
        self._ui.actionUndo.setEnabled(False)

    def enable_redo(self):
        self._ui.actionRedo.setEnabled(True)

    def disable_redo(self):
        self._ui.actionRedo.setEnabled(False)

    def print_lines_to_history(self, lines: str):
        self._ui.history.append(lines)

    def delete_from_history(self, number_of_lines: int = 1):
        history = self._ui.history.toPlainText()
        history = history.split('\n')

        if number_of_lines > len(history):
            raise ValueError

        history = history[:(-number_of_lines)]
        history = '\n'.join(history)
        self._ui.history.setText(history)
        self._ui.history.moveCursor(QTextCursor.End)
        self._ui.history.ensureCursorVisible()

    def clear_history(self):
        self._ui.history.setText('')
