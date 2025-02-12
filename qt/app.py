from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QToolBar, QStackedWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.uic import loadUi
import sys
import os

base_path = os.path.dirname(__file__)


def switch_to_scr1():
    stacked_widget.setCurrentWidget(screen1)
    current_screen = stacked_widget.currentWidget()
    for action in current_screen.toolBar.actions():
        action.setDisabled(False)
    current_screen.actionScreen1.setDisabled(True)
    stacked_widget.setWindowTitle("Screen 1")


def switch_to_scr2():
    stacked_widget.setCurrentWidget(screen2)
    current_screen = stacked_widget.currentWidget()
    for action in current_screen.toolBar.actions():
        action.setDisabled(False)
    current_screen.actionScreen2.setDisabled(True)
    stacked_widget.setWindowTitle("Screen 2")


def switch_to_scr3():
    stacked_widget.setCurrentWidget(screen3)
    current_screen = stacked_widget.currentWidget()
    for action in current_screen.toolBar.actions():
        action.setDisabled(False)
    current_screen.actionScreen3.setDisabled(True)
    stacked_widget.setWindowTitle("Screen 3")

class Screen1(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi(f'{base_path}/main.ui', self)

        self.actionScreen1.triggered.connect(switch_to_scr1)
        self.actionScreen2.triggered.connect(switch_to_scr2)
        self.actionScreen3.triggered.connect(switch_to_scr3)
        self.label.setText("Screen 1")



class Screen2(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi(f'{base_path}/main.ui', self)

        self.actionScreen1.triggered.connect(switch_to_scr1)
        self.actionScreen2.triggered.connect(switch_to_scr2)
        self.actionScreen3.triggered.connect(switch_to_scr3)
        self.label.setText("Screen 2")

class Screen3(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi(f'{base_path}/main.ui', self)

        self.actionScreen1.triggered.connect(switch_to_scr1)
        self.actionScreen2.triggered.connect(switch_to_scr2)
        self.actionScreen3.triggered.connect(switch_to_scr3)
        self.label.setText("Screen 3")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    screen1 = Screen1()
    stacked_widget.addWidget(screen1)

    screen2 = Screen2()
    stacked_widget.addWidget(screen2)

    screen3 = Screen3()
    stacked_widget.addWidget(screen3)

    switch_to_scr1()
    stacked_widget.setMinimumSize(800, 600)
    stacked_widget.show()

    app.exec()
