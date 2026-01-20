from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt

from app.service.movie_service import search_movies


class SearchByTitlePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите название фильма")
        self.btn_search = QPushButton("Поиск")

        search_layout.addWidget(self.input)
        search_layout.addWidget(self.btn_search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Название", "Год", "Актёры", "Просмотрен"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)

        self.btn_search.clicked.connect(self.search)

    def search(self):
        title = self.input.text().strip()
        if not title:
            return

        movies = search_movies(title)

        self.table.setRowCount(len(movies))

        for row, movie in enumerate(movies):
            self.table.setItem(row, 0, QTableWidgetItem(movie.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(movie.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in movie.actors))
            )

            watched = QTableWidgetItem("✔" if movie.watched else "—")
            watched.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, watched)

        self.table.resizeColumnsToContents()
