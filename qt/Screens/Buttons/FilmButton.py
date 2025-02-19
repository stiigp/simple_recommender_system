from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QToolBar, \
    QStackedWidget, QSizePolicy
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.uic import loadUi
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

class FilmButton(QPushButton):
    poster: QIcon
    title: QLabel

    def __init__(self, poster: QIcon, title: QLabel):
        super().__init__(title)

        self.setFixedSize(100, 150)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setIcon(poster)
        self.setIconSize(self.size())
