from PyQt5.QtWidgets import QMainWindow

from .ui.appgui import Ui_MainWindow
from .utils import resource_path

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        resource_path('Logo.svg')
