import os
import sys

from PyQt5 import QtWidgets

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.exec()
