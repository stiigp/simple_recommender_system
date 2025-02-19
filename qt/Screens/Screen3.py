from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QToolBar, QStackedWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.uic import loadUi
from qt.Screens.ScreenSwitch import switch_to_scr
import os

base_path = os.path.dirname(__file__)

class Screen3(QMainWindow):
    def __init__(self):
        super().__init__()


        loadUi(base_path + '/../main.ui', self)

        self.actionScreen1.triggered.connect(lambda: switch_to_scr(self.parent(), 0))
        self.actionScreen2.triggered.connect(lambda: switch_to_scr(self.parent(), 1))
        self.actionScreen3.triggered.connect(lambda: switch_to_scr(self.parent(), 2))
        self.label.setText("Screen 3")