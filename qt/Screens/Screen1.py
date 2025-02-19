from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QSizePolicy
from PyQt5.QtCore import QUrl
from PyQt5.uic import loadUi
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from qt.Screens.Buttons.FilmButton import FilmButton
import os
import json
from qt.Screens.ScreenSwitch import switch_to_scr
from treating_data.best_average_ratings import grouped_by_mean
from thefuzz import process
from typing import List

base_path = os.path.dirname(__file__)
treating_data_path = os.path.dirname(os.path.dirname(base_path))


class Screen1(QMainWindow):

    current_page = 0
    buttons_per_page = 9
    manager = QNetworkAccessManager()

    def get_urls_as_dictionary(self):
        urls_file = open(treating_data_path + '/treating_data/poster_urls.json')
        urls = json.load(urls_file)

        return urls

    def get_titles_from_poster_urls(self, urls: dict) -> List:
        return [film['title'] for film in urls]

    def getting_titles_and_posters_urls(self, start: int, max_characters: int=25, number_of_titles_per_page: int=9) -> dict[str:str]:

        urls = self.get_urls_as_dictionary()

        res = {}

        for index, row in grouped_by_mean.iloc[start : start + number_of_titles_per_page].iterrows():
            title = row['title'][:-7]
            if title[-5:] == ", The":
                title = "The " + title[:-5]

            if len(title) > max_characters:
                name = title[:max_characters]
                name += "..."
            else:
                name = title

            titles_from_urls = self.get_titles_from_poster_urls(urls)
            url_title = process.extractOne(query=title, choices=titles_from_urls)[0]

            for item in urls:
                if item['title'] == url_title:
                    # poster_url = item['poster_url']
                    res[name] = item['poster_url']

        return res

    def on_image_downloaded(self, reply, button) -> QPixmap:
        # gera e retorna
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll())
        # pixmap = pixmap.scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        print(pixmap.size())

        button.setIcon(QIcon(pixmap))
        # button.setIconSize(button.size())



    def load_buttons(self):
        column_index = 0
        row_index = 0

        titles_and_urls = self.getting_titles_and_posters_urls(start=self.current_page * self.buttons_per_page)
        self.current_page += 1

        for title, url in titles_and_urls.items():

            button = QPushButton(title)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMaximumSize(200, 300)

            reply = self.manager.get(QNetworkRequest(QUrl(url)))
            reply.finished.connect(lambda: self.on_image_downloaded(reply, button))

            self.gridLayout.addWidget(button, row_index, column_index)

            column_index += 1
            if column_index == 3:
                column_index = 0
                row_index += 1

            if row_index == 3:
                break

    def __init__(self):
        super().__init__()

        loadUi(base_path + '/../scr1.ui', self)

        self.actionScreen1.triggered.connect(lambda: switch_to_scr(self.parent(), 0))
        self.actionScreen2.triggered.connect(lambda: switch_to_scr(self.parent(), 1))
        self.actionScreen3.triggered.connect(lambda: switch_to_scr(self.parent(), 2))

        # self.load_buttons()
        meu_button = QPushButton()
        if not os.path.exists("C:/Users/Usuario\Desktop\CODING\simple_recommender_system\qt\Screens\Buttons/test_poster.jpg"):
            print("Arquivo não encontrado!")
        meu_button.setStyleSheet("""
            QPushButton {
                background-image: url(C:/Users/Usuario\Desktop\CODING\simple_recommender_system\qt\Screens\Buttons/test_poster.jpg);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)
        meu_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        meu_button.setMaximumSize(500, 750)
        self.gridLayout.addWidget(meu_button, 0, 0)
