import pytest

from app.command_engine import CommandEngine
from app.commands import Command


class ControllerMockup:
    def __init__(self):
        self.undo = False
        self.redo = False
        self.command_engine = None

    def enable_undo(self):
        self.undo = True

    def disable_undo(self):
        self.undo = False

    def enable_redo(self):
        self.redo = True

    def disable_redo(self):
        self.redo = False

    def execute_command(self, command: Command, from_redo: bool = False):
        self.command_engine.execute_command(command, from_redo=from_redo)


class CommandMockup(Command):
    def __init__(self, receiver):
        super().__init__(receiver)
        self.executed = 0
        self.reversed = 0

    def execute(self):
        self.executed += 1

    def reverse(self):
        self.reversed += 1


@pytest.fixture
def command_engine() -> CommandEngine:
    controller = ControllerMockup()
    command_engine = CommandEngine(controller)
    controller.command_engine = command_engine
    return command_engine


def test_execute_command(command_engine: CommandEngine):
    command_engine._redos = [1, 'invalid', None]
    command_engine._controller.enable_redo()
    command = CommandMockup(None)
    command_engine.execute_command(command)

    assert command_engine._undos == [command]
    assert command_engine._controller.undo is True
    assert command_engine._controller.redo is False
    assert command_engine._redos == []
    assert command.executed == 1


def test_remove_last_command(command_engine: CommandEngine):
    c1 = CommandMockup('receiver')
    c2 = CommandMockup(123)
    command_engine.execute_command(c1)
    command_engine.execute_command(c2)

    command_engine.remove_last_command()
    assert command_engine._undos == [c1]

    command_engine.remove_last_command()
    assert command_engine._undos == []


def test_undo(command_engine: CommandEngine):
    c1 = CommandMockup('receiver')
    c2 = CommandMockup(123)
    command_engine.execute_command(c1)
    command_engine.execute_command(c2)

    command_engine.undo()
    assert command_engine._undos == [c1]
    assert command_engine._redos == [c2]
    assert c2.reversed == 1
    assert command_engine._controller.redo is True

    command_engine.undo()
    assert command_engine._undos == []
    assert command_engine._redos == [c2, c1]
    assert c1.reversed == 1
    assert command_engine._controller.undo is False


def test_redo(command_engine: CommandEngine):
    c1 = CommandMockup('receiver')
    c2 = CommandMockup(123)
    command_engine.execute_command(c1)
    command_engine.execute_command(c2)
    command_engine.undo()
    command_engine.undo()

    command_engine.redo()
    assert command_engine._undos == [c1]
    assert command_engine._redos == [c2]
    assert command_engine._controller.undo is True
    assert c1.executed == 2

    command_engine.redo()
    assert command_engine._undos == [c1, c2]
    assert command_engine._redos == []
    assert command_engine._controller.redo is False
    assert c2.executed == 2


def test_get_all_commands(command_engine: CommandEngine):
    c1 = CommandMockup('receiver')
    c2 = CommandMockup(123)
    command_engine.execute_command(c1)
    command_engine.execute_command(c2)
    command_engine.undo()
    command_engine.undo()
    command_engine.redo()

    res = command_engine.get_all_commands()
    assert res['undos'] == [c1]
    assert res['redos'] == [c2]
