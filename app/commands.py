class Command:
    def __init__(self, receiver):
        self._receiver = receiver

    def execute(self):
        pass

    def reverse(self):
        pass


class PaintRectCommand(Command):
    def execute(self):
        self._receiver.draw_rectangle()
