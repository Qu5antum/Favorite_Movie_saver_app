from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
import webbrowser

from app.database.db import session
from app.service.movie_service import MovieService


class SearchMovieByActorPage(QWidget):
    URL_COL = 4  # индекс колонки для ссылки

    def __init__(self, stack):
        super().__init__()
        self.stack = stack  # для кнопки Назад

        self.session = session
        self.movie_service = MovieService(session=session)

        layout = QVBoxLayout(self)

        # Поле поиска
        search_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите имя актёра из фильма")
        self.btn_search = QPushButton("Поиск")
        search_layout.addWidget(self.input)
        search_layout.addWidget(self.btn_search)
        layout.addLayout(search_layout)

        # Таблица с результатами
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Название Фильма", "Год", "Актёры", "Просмотрен", "Ссылка"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)
        layout.addWidget(self.table)

        # Кнопка Назад
        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        # Кнопка поиска
        self.btn_search.clicked.connect(self.search)

    def go_back(self):
        self.stack.setCurrentIndex(1) 

    def search(self):
        actor_name = self.input.text().strip()
        if not actor_name:
            return

        movies = self.movie_service.filter_movies_by_actor(actor_name)

        self.table.setRowCount(len(movies))

        for row, movie in enumerate(movies):
            self.table.setItem(row, 0, QTableWidgetItem(movie.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(movie.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in movie.movie_actors))
            )

            watched_item = QTableWidgetItem("+" if movie.watched else "-")
            watched_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, watched_item)

            # Ссылка
            url_item = QTableWidgetItem(movie.url or "")
            url_item.setData(Qt.UserRole, movie.url)
            url_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.URL_COL, url_item)

        self.table.resizeColumnsToContents()

    def on_cell_clicked(self, row, column):
        if column == self.URL_COL:
            item = self.table.item(row, column)
            url = item.data(Qt.UserRole)
            if url:
                webbrowser.open(url)