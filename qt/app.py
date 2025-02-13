from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QToolBar, QStackedWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.uic import loadUi
from Screens.Screen1 import Screen1
from Screens.Screen2 import Screen2
from Screens.Screen3 import Screen3
from Screens.ScreenSwitch import switch_to_scr
import sys
import os

base_path = os.path.dirname(__file__)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    screen1 = Screen1()
    stacked_widget.addWidget(screen1)

    screen2 = Screen2()
    stacked_widget.addWidget(screen2)

    screen3 = Screen3()
    stacked_widget.addWidget(screen3)

    switch_to_scr(stacked_widget, 0)
    stacked_widget.setMinimumSize(800, 600)
    stacked_widget.show()

    app.exec()
