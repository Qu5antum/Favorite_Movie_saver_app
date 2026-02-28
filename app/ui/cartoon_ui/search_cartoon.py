from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
import webbrowser

from app.database.db import session
from app.service.cartoon_service import CartoonService


class SearchCartoonByTitlePage(QWidget):
    WATCHED_COL = 3
    URL_COL = 4 

    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.session = session
        self.cartoon_service = CartoonService(session=self.session)

        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите название мультфильма")
        self.btn_search = QPushButton("Поиск")
        search_layout.addWidget(self.input)
        search_layout.addWidget(self.btn_search)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Название Мультфильма", "Год", "Тип", "Просмотрен", "Ссылка"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)

        self.btn_search.clicked.connect(self.search)

    def go_back(self):
        self.stack.setCurrentIndex(3)

    def search(self):
        title = self.input.text().strip()
        if not title:
            return

        cartoons = self.cartoon_service.search_cartoon_by_title(title)

        self.table.setRowCount(len(cartoons))

        for row, cartoon in enumerate(cartoons):
            self.table.setItem(row, 0, QTableWidgetItem(cartoon.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(cartoon.year)))
            self.table.setItem(row, 2, QTableWidgetItem(cartoon.cartoon_type))

            watched_item = QTableWidgetItem("+" if cartoon.watched else "-")
            watched_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.WATCHED_COL, watched_item)

            # ссылка
            url_item = QTableWidgetItem(cartoon.url or "")
            url_item.setForeground(Qt.blue)
            url_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            url_item.setData(Qt.UserRole, cartoon.url)
            self.table.setItem(row, self.URL_COL, url_item)

        self.table.resizeColumnsToContents()

    def on_cell_clicked(self, row, column):
        if column == self.URL_COL:
            url_item = self.table.item(row, column)
            url = url_item.data(Qt.UserRole)
            if url:
                webbrowser.open(url)