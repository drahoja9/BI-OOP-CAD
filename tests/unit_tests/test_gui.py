import pytest
from pytestqt.qtbot import QtBot

from app.brushes import LineShapeBrush, CircleShapeBrush, MoveShapeBrush
from app.commands import Command, ClearCommand, SaveCommand, LoadCommand, QuitCommand
from app.gui import MainWindow


class ControllerMockup:
    def __init__(self):
        self.parsed = ''
        self.command = None

    def parse_command(self, command_text: str):
        self.parsed = command_text

    def execute_command(self, command: Command):
        self.command = command


@pytest.fixture
def gui(qtbot: QtBot) -> MainWindow:
    controller = ControllerMockup()
    gui = MainWindow(controller)
    qtbot.addWidget(gui)
    return gui


def test_handle_action_new(gui: MainWindow):
    gui._handle_action_new()
    assert gui._controller.command == ClearCommand(gui._controller)


def test_handle_save_file(gui: MainWindow):
    gui._handle_save_file()
    assert gui._controller.command == SaveCommand(gui._controller)


def test_handle_load_file(gui: MainWindow):
    gui._handle_load_file()
    assert gui._controller.command == LoadCommand(gui._controller)


def test_handle_action_quit(gui: MainWindow):
    gui._handle_action_quit()
    assert gui._controller.command == QuitCommand(gui._controller)


def test_set_status(gui: MainWindow):
    assert gui.statusBar().currentMessage() == 'Move'
    gui.set_status('Rectangle')
    assert gui.statusBar().currentMessage() == 'Rectangle'
    gui.set_status()
    assert gui.statusBar().currentMessage() == 'Move'


def test_toggle_brush(gui: MainWindow):
    assert gui.canvas.brush == MoveShapeBrush()
    assert gui.statusBar().currentMessage() == 'Move'
    for brush_button in gui.brush_buttons.values():
        assert brush_button.isChecked() is False

    button = gui.brush_buttons[LineShapeBrush()]
    button.click()
    assert gui.canvas.brush is LineShapeBrush()
    assert gui.statusBar().currentMessage() == 'Line'
    assert button.isChecked() is True

    button = gui.brush_buttons[CircleShapeBrush()]
    button.click()
    assert gui.canvas.brush is CircleShapeBrush()
    assert gui.statusBar().currentMessage() == 'Circle'
    assert gui.brush_buttons[LineShapeBrush()].isChecked() is False
    assert button.isChecked() is True

    button.click()
    assert gui.canvas.brush == MoveShapeBrush()
    assert gui.statusBar().currentMessage() == 'Move'
    assert button.isChecked() is False


def test_handle_user_input(gui: MainWindow):
    gui._ui.manualInput.setText('test input 123')
    gui._handle_user_input()
    assert gui._ui.manualInput.text() == ''
    assert gui._controller.parsed == 'test input 123'

    gui._ui.manualInput.setText('')
    gui._handle_user_input()
    assert gui._ui.manualInput.text() == ''
    assert gui._controller.parsed == 'test input 123'

    gui._ui.manualInput.setText('     \n     \t     ')
    gui._handle_user_input()
    assert gui._ui.manualInput.text() == ''
    assert gui._controller.parsed == 'test input 123'


def test_undo(gui: MainWindow):
    assert gui._ui.actionUndo.isEnabled() is False
    gui.enable_undo()
    assert gui._ui.actionUndo.isEnabled() is True
    gui.enable_undo()
    assert gui._ui.actionUndo.isEnabled() is True
    gui.disable_undo()
    assert gui._ui.actionUndo.isEnabled() is False


def test_redo(gui: MainWindow):
    assert gui._ui.actionRedo.isEnabled() is False
    gui.enable_redo()
    assert gui._ui.actionRedo.isEnabled() is True
    gui.enable_redo()
    assert gui._ui.actionRedo.isEnabled() is True
    gui.disable_redo()
    assert gui._ui.actionRedo.isEnabled() is False


def test_print_lines_to_history(gui: MainWindow):
    assert gui._ui.history.toPlainText() == ''
    gui.print_lines_to_history('new line printed to the history \n actualy it\'s two lines')
    assert gui._ui.history.toPlainText() == 'new line printed to the history \n actualy it\'s two lines'
    gui.print_lines_to_history('yet another line')
    assert (
        gui._ui.history.toPlainText()
        ==
        'new line printed to the history \n actualy it\'s two lines\nyet another line'
    )


def test_delete_from_history(gui: MainWindow):
    gui.print_lines_to_history('line1')
    gui.print_lines_to_history('line2')
    gui.print_lines_to_history('line3')
    gui.print_lines_to_history('line4')

    gui.delete_from_history(1)
    assert gui._ui.history.toPlainText() == 'line1\nline2\nline3'

    gui.delete_from_history(3)
    assert gui._ui.history.toPlainText() == ''

    with pytest.raises(ValueError):
        gui.delete_from_history(123)


def test_clear_history(gui: MainWindow):
    gui.print_lines_to_history('line1')
    gui.print_lines_to_history('line2')
    gui.print_lines_to_history('line3')
    gui.print_lines_to_history('line4')

    gui.clear_history()
    assert gui._ui.history.toPlainText() == ''
