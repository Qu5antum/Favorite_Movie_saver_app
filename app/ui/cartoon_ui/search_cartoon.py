from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt

from app.database.db import session
from app.service.cartoon_service import CartoonService


class SearchCartoonByTitlePage(QWidget):
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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Название Фильма", "Год", "Тип", "Просмотрен"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

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
            self.table.setItem(row, 2,QTableWidgetItem(cartoon.cartoon_type))

            watched = QTableWidgetItem("+" if cartoon.watched else "-")
            watched.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, watched)

        self.table.resizeColumnsToContents()
