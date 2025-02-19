from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QToolBar, \
    QStackedWidget, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.uic import loadUi
import os
import json
from qt.Screens.ScreenSwitch import switch_to_scr
from treating_data.best_average_ratings import grouped_by_mean
from thefuzz import process

class Screen1(QMainWindow):
    def __init__(self):
        super().__init__()

        base_path = os.path.dirname(__file__)
        treating_data_path = os.path.dirname(os.path.dirname(base_path))
        urls_file = open(treating_data_path + '/treating_data/poster_urls.json')
        urls = json.load(urls_file)

        loadUi(base_path + '/../scr1.ui', self)

        self.actionScreen1.triggered.connect(lambda: switch_to_scr(self.parent(), 0))
        self.actionScreen2.triggered.connect(lambda: switch_to_scr(self.parent(), 1))
        self.actionScreen3.triggered.connect(lambda: switch_to_scr(self.parent(), 2))

        row_number = column_number = 0
        max_characters = 25
        titles_from_poster_urls = [film['title'] for film in urls]

        for index, row in grouped_by_mean.iterrows():
            # print(row['title'])
            # title = process.extract(row['title'], titles)[0][0]
            # print(title)
            title = row['title'][:-7]
            if title[-5:] == ", The":
                title = "The " + title[:-5]

            if len(title) > max_characters:
                name = title[:max_characters]
                name += "..."
            else:
                name = title

            url_title = process.extractOne(query=title, choices=titles_from_poster_urls)



            pixmap = QPixmap("")
            icon = QIcon(pixmap)
            button = QPushButton(name)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.setIcon(icon)
            self.gridLayout.addWidget(button, row_number, column_number)

            column_number += 1
            if column_number == 3:
                column_number = 0
                row_number += 1

            if row_number == 3:
                break
