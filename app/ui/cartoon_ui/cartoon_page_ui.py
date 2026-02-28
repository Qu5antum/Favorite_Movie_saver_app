from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PySide6.QtGui import QIcon

from .add_cartoon_ui import AddCartoonPage
from .get_cartoon_ui import AllCartoonPage
from .search_cartoon import SearchCartoonByTitlePage


class CartoonPage(QWidget):
    def __init__(self, stack: QStackedWidget):
        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        layout.addWidget(QLabel("🧸 Страница мультфильмов"))

        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ Добавить мультфильм")
        self.btn_all = QPushButton("📄 Все мультфильмы")
        self.btn_search = QPushButton("🔍 Поиск мультфильма")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_all)
        btn_layout.addWidget(self.btn_search)

        layout.addLayout(btn_layout)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(lambda: stack.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.add_page = AddCartoonPage(self.stack)
        self.all_page = AllCartoonPage(self.stack)
        self.search_page = SearchCartoonByTitlePage(self.stack)

        self.btn_add.clicked.connect(lambda: self.open_page(self.add_page))
        self.btn_all.clicked.connect(lambda: self.open_page(self.all_page))
        self.btn_search.clicked.connect(lambda: self.open_page(self.search_page))

    def open_page(self, page: QWidget):
        if self.stack.indexOf(page) == -1:
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)