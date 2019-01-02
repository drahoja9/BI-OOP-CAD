import pytest
from pytestqt.qtbot import QtBot

from app.brushes import LineShapeBrush, CircleShapeBrush, MoveShapeBrush
from app.gui import MainWindow


class ControllerMockup:
    def __init__(self):
        self.restarted = False

    def restart(self):
        self.restarted = True


@pytest.fixture
def gui(qtbot: QtBot) -> MainWindow:
    controller = ControllerMockup()
    gui = MainWindow(controller)
    qtbot.addWidget(gui)
    return gui


def test_handle_new_action(gui: MainWindow):
    assert gui._controller.restarted is False
    gui._handle_new_action()
    assert gui._controller.restarted is True


def test_set_status(gui: MainWindow):
    assert gui.statusBar().currentMessage() == 'Move'
    gui._set_status('Rectangle')
    assert gui.statusBar().currentMessage() == 'Rectangle'
    gui._set_status()
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
    assert gui._handle_user_input() == 'test input 123'
    assert gui._ui.manualInput.text() == ''


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


def test_print_newline_to_history(gui: MainWindow):
    assert gui._ui.history.toPlainText() == ''
    gui.print_newline_to_history('new line printed to the history \n actualy it\'s two lines')
    assert gui._ui.history.toPlainText() == 'new line printed to the history \n actualy it\'s two lines'
    gui.print_newline_to_history('yet another line')
    assert (
        gui._ui.history.toPlainText()
        ==
        'new line printed to the history \n actualy it\'s two lines\nyet another line'
    )


def test_delete_from_history(gui: MainWindow):
    gui.print_newline_to_history('line1')
    gui.print_newline_to_history('line2')
    gui.print_newline_to_history('line3')
    gui.print_newline_to_history('line4')

    gui.delete_from_history(1)
    assert gui._ui.history.toPlainText() == 'line1\nline2\nline3'

    gui.delete_from_history(3)
    assert gui._ui.history.toPlainText() == ''

    with pytest.raises(ValueError):
        gui.delete_from_history(123)


def test_clear_history(gui: MainWindow):
    gui.print_newline_to_history('line1')
    gui.print_newline_to_history('line2')
    gui.print_newline_to_history('line3')
    gui.print_newline_to_history('line4')

    gui.clear_history()
    assert gui._ui.history.toPlainText() == ''
