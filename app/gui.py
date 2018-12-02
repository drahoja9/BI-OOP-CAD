from PyQt5 import QtWidgets

from app.ui.main_window import Ui_MainWindow
from app.canvas import Canvas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        # We have to create the Qt application first
        self._app = QtWidgets.QApplication([])
        super().__init__()
        self._ui = Ui_MainWindow()
        self.canvas = Canvas(controller)

        self._ui.setupUi(self)
        self._ui.scrollArea.setWidget(self.canvas)

    def run(self):
        self.show()
        self._app.exec()
