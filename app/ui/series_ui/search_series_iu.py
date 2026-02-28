from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt
import webbrowser

from app.database.db import session
from app.service.series_service import SeriesService


class SearchSeriesByTitlePage(QWidget):
    URL_COL = 4 

    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.session = session
        self.series_service = SeriesService(session=session)

        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите название сериала")
        self.btn_search = QPushButton("Поиск")
        search_layout.addWidget(self.input)
        search_layout.addWidget(self.btn_search)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Название Сериала", "Год", "Актёры", "Просмотрен", "Ссылка"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.open_url_from_cell)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        self.btn_search.clicked.connect(self.search)

    def go_back(self):
        self.stack.setCurrentIndex(2) 

    def search(self):
        title = self.input.text().strip()
        if not title:
            return

        serieses = self.series_service.search_serises(title)
        self.table.setRowCount(len(serieses))

        for row, series in enumerate(serieses):
            self.table.setItem(row, 0, QTableWidgetItem(series.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(series.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in series.series_actors))
            )

            watched_item = QTableWidgetItem("+" if series.watched else "-")
            watched_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, watched_item)

            url_item = QTableWidgetItem(series.url or "")
            url_item.setForeground(Qt.blue)
            url_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.URL_COL, url_item)

        self.table.resizeColumnsToContents()

    def open_url_from_cell(self, row, column):
        if column == self.URL_COL:
            url_item = self.table.item(row, column)
            url = url_item.text().strip()
            if url:
                webbrowser.open(url)
            else:
                QMessageBox.information(self, "Информация", "Ссылка отсутствует")