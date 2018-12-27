import os
import sys

from PyQt5 import QtWidgets


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.controller import Controller


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    controller = Controller()
    controller.run_app()

    # Wrapping the GUI execution into `sys.exit()` to ensure that proper result code
    # will be returned when the window closes (otherwise it's always 0)
    sys.exit(app.exec())
