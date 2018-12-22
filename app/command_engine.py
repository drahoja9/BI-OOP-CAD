from typing import List, Dict

from app.commands import Command


class CommandEngine:
    def __init__(self, controller):
        self._controller = controller
        self._undos = []
        self._redos = []

    def _push_undo(self, command: Command):
        if not self._undos:
            self._controller.enable_undo()
        self._undos.append(command)

    def _pop_undo(self) -> Command:
        command = self._undos.pop()
        if not self._undos:
            self._controller.disable_undo()
        return command

    def _push_redo(self, command: Command):
        if not self._redos:
            self._controller.enable_redo()
        self._redos.append(command)

    def _pop_redo(self) -> Command:
        command = self._redos.pop()
        if not self._redos:
            self._controller.disable_redo()
        return command

    def execute_command(self, command: Command, from_redo: bool = False):
        self._push_undo(command)
        if not from_redo:
            self._redos = []
            self._controller.disable_redo()
        command.execute()

    def undo(self):
        command = self._pop_undo()
        command.reverse()
        self._push_redo(command)

    def redo(self):
        command = self._pop_redo()
        self.execute_command(command, from_redo=True)

    def get_all_commands(self) -> Dict[str, List[Command]]:
        return {'undos': self._undos, 'redos': self._redos}

    def restart(self):
        self._undos = []
        self._redos = []
        self._controller.disable_undo()
        self._controller.disable_redo()
