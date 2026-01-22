from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from app.service.movie_service import get_all_movies, update_watched_movie, delete_movie_by_id


class AllMoviesPage(QWidget):
    WATCHED_COL = 3

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Все фильмы")

        self.current_order = None

        layout = QVBoxLayout(self)

        filter_layout = QHBoxLayout()

        self.btn_all = QPushButton("Все")
        self.btn_old = QPushButton("Старые")
        self.btn_new = QPushButton("Новые")

        self.btn_all.clicked.connect(lambda: self.set_filter(None))
        self.btn_old.clicked.connect(lambda: self.set_filter("asc"))
        self.btn_new.clicked.connect(lambda: self.set_filter("desc"))

        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_old)
        filter_layout.addWidget(self.btn_new)

        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Название Фильма", "Год", "Актёры", "Просмотрен"]
        )

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.itemChanged.connect(self.on_watched_changed)

        layout.addWidget(self.table)

        self.btn_delete = QPushButton("Удалить фильм")
        layout.addWidget(self.btn_delete)

        self.btn_delete.clicked.connect(self.delete_movie)

    def set_filter(self, order: str | None):
        self.current_order = order
        self.load_movies()

    def load_movies(self):
        movies = get_all_movies(self.current_order)

        self.table.blockSignals(True) 
        self.table.setRowCount(len(movies))

        for row, movie in enumerate(movies):
            self.table.setItem(row, 0, QTableWidgetItem(movie.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(movie.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in movie.movie_actors))
            )

            watched_item = QTableWidgetItem()
            watched_item.setFlags(
                Qt.ItemIsSelectable |
                Qt.ItemIsEnabled |
                Qt.ItemIsUserCheckable
            )
            watched_item.setCheckState(
                Qt.Checked if movie.watched else Qt.Unchecked
            )

            # сохраняем movie_id
            watched_item.setData(Qt.UserRole, movie.id)
            watched_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, self.WATCHED_COL, watched_item)

        self.table.blockSignals(False)  
        self.table.resizeColumnsToContents()

    def on_watched_changed(self, item: QTableWidgetItem):
        if item.column() != self.WATCHED_COL:
            return

        movie_id = item.data(Qt.UserRole)
        watched = item.checkState() == Qt.Checked

        update_watched_movie(movie_id, watched)
    
    def delete_movie(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите фильм для удаления"
            )
            return

        item = self.table.item(row, self.WATCHED_COL)
        movie_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить выбранный фильм?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        success = delete_movie_by_id(movie_id)

        if success:
            self.load_movies()
        else:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось удалить фильм"
            )

