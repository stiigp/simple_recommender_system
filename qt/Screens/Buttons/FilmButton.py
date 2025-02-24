from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QToolBar, \
    QStackedWidget, QSizePolicy
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.uic import loadUi
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

class FilmButton(QWidget):
    def __init__(self, img_path: str, title: str):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.setMinimumSize(100, 150)
        self.setMaximumSize(198, 299)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # QLabel que vai representar a imagem
        self.image_label = QLabel(self)
        pixmap = QPixmap(img_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        # QLabel que vai representar o titulo
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); padding: 5px;")
        self.title_label.setVisible(False)

        # adicionando os títulos ao layout
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.title_label)

        # isso aparentemente permite manipular eventos de mouse
        self.setMouseTracking(True)

    def enterEvent(self, a0):
        self.title_label.setVisible(True)

    def leaveEvent(self, a0):
        self.title_label.setVisible(False)

    def mousePressEvent(self, a0):
        if a0.button() == Qt.LeftButton:
            print(f"Filme {self.title_label.text()} selecionado!")

    def sizeHint(self):
        return QSize(200, 300)
