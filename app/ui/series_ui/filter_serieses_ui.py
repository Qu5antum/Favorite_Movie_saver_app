from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt
import webbrowser

from app.database.db import session
from app.service.series_service import SeriesService


class SearchSeriesByActorPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.session = session
        self.series_service = SeriesService(session=self.session)

        self.setWindowTitle("Поиск сериала по актёру")

        layout = QVBoxLayout(self)

        # --- Поисковая панель ---
        search_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите имя актёра из сериала")
        self.btn_search = QPushButton("Поиск")
        search_layout.addWidget(self.input)
        search_layout.addWidget(self.btn_search)

        # --- Таблица результатов ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Название Сериала", "Год", "Актёры", "Просмотрен", "Ссылка"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.open_url_from_cell)

        # --- Кнопка Назад ---
        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.btn_search.clicked.connect(self.search)

    def go_back(self):
        self.stack.setCurrentIndex(2) 

    def search(self):
        actor_name = self.input.text().strip()
        if not actor_name:
            return

        serieses = self.series_service.filter_serieses_by_actor(actor_name)

        self.table.setRowCount(len(serieses))

        for row, series in enumerate(serieses):
            self.table.setItem(row, 0, QTableWidgetItem(series.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(series.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in series.series_actors))
            )

            watched = QTableWidgetItem("+" if series.watched else "-")
            watched.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, watched)

            # Добавляем ссылку
            url_item = QTableWidgetItem(series.url or "")
            url_item.setTextAlignment(Qt.AlignCenter)
            url_item.setForeground(Qt.blue)
            self.table.setItem(row, 4, url_item)

        self.table.resizeColumnsToContents()

    def open_url_from_cell(self, row, column):
        # Открываем ссылку в браузере, если кликнули по колонке URL
        if column == 4:
            url_item = self.table.item(row, column)
            url = url_item.text().strip()
            if url:
                webbrowser.open(url)
            else:
                QMessageBox.information(self, "Информация", "Ссылка отсутствует")