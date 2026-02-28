from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
import webbrowser

from app.database.db import session
from app.service.movie_service import MovieService


class AllMoviesPage(QWidget):
    WATCHED_COL = 3
    URL_COL = 4

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Все фильмы")

        self.session = session
        self.movie_service = MovieService(session=session)

        self.current_order = None
        self.current_watched = None 

        layout = QVBoxLayout(self)

        filter_layout = QHBoxLayout()
        self.btn_all = QPushButton("Все")
        self.btn_old = QPushButton("Старые")
        self.btn_new = QPushButton("Новые")
        self.btn_watched = QPushButton("Смотрел")
        self.btn_no_watched = QPushButton("Не Смотрел")

        self.btn_all.clicked.connect(self.reset_filters)
        self.btn_old.clicked.connect(lambda: self.set_filter("asc"))
        self.btn_new.clicked.connect(lambda: self.set_filter("desc"))
        self.btn_watched.clicked.connect(lambda: self.set_watched_filter(True))
        self.btn_no_watched.clicked.connect(lambda: self.set_watched_filter(False))

        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_old)
        filter_layout.addWidget(self.btn_new)
        filter_layout.addWidget(self.btn_watched)
        filter_layout.addWidget(self.btn_no_watched)
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Название Фильма", "Год", "Актёры", "Просмотрен", "Ссылка"]
        )

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)
        self.table.itemChanged.connect(self.on_watched_changed)
        layout.addWidget(self.table)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)

        self.btn_delete = QPushButton("Удалить фильм")
        layout.addWidget(self.btn_delete)
        self.btn_delete.clicked.connect(self.delete_movie)
        layout.addWidget(back_btn)

    def go_back(self):
        self.stack.setCurrentIndex(1)
    
    def reset_filters(self):
        self.current_order = None
        self.current_watched = None
        self.load_movies()

    def set_watched_filter(self, watched: bool | None):
        self.current_watched = watched
        self.load_movies()

    def set_filter(self, order: str | None):
        self.current_order = order
        self.load_movies()

    def load_movies(self):
        movies = self.movie_service.get_all_movies(
            watched=self.current_watched,
            order=self.current_order
        )
        
        self.table.blockSignals(True) 
        self.table.setRowCount(len(movies))

        for row, movie in enumerate(movies):
            self.table.setItem(row, 0, QTableWidgetItem(movie.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(movie.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in movie.movie_actors))
            )

            # Просмотрен
            watched_item = QTableWidgetItem()
            watched_item.setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
            )
            watched_item.setCheckState(Qt.Checked if movie.watched else Qt.Unchecked)
            watched_item.setData(Qt.UserRole, movie.id)
            watched_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.WATCHED_COL, watched_item)

            # Ссылка
            url_item = QTableWidgetItem(movie.url or "")
            url_item.setData(Qt.UserRole, movie.url)
            url_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.URL_COL, url_item)

        self.table.blockSignals(False)  
        self.table.resizeColumnsToContents()

    def on_watched_changed(self, item: QTableWidgetItem):
        if item.column() != self.WATCHED_COL:
            return
        movie_id = item.data(Qt.UserRole)
        watched = item.checkState() == Qt.Checked
        self.movie_service.update_watched_movie(movie_id, watched)

    def on_cell_clicked(self, row, column):
        if column == self.URL_COL:
            item = self.table.item(row, column)
            url = item.data(Qt.UserRole)
            if url:
                webbrowser.open(url)

    def delete_movie(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите фильм для удаления")
            return

        item = self.table.item(row, self.WATCHED_COL)
        movie_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Удалить выбранный фильм?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        success = self.movie_service.delete_movie_by_id(movie_id)
        if success:
            self.load_movies()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить фильм")