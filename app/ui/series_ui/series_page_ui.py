from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PySide6.QtGui import QIcon

from .add_series_ui import AddSeriesPage
from .filter_serieses_ui import SearchSeriesByActorPage
from .get_serieses_ui import AllSeriesPage
from .search_series_iu import SearchSeriesByTitlePage

class SeriesPage(QWidget):
    def __init__(self, stack: QStackedWidget):
        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📺 Страница сериалов"))

        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ Добавить Сериал")
        self.btn_all = QPushButton("📄 Все сериалы")
        self.btn_search = QPushButton("🔍 Поиск сериалов")
        self.btn_search_by_actor = QPushButton("🎭 Поиск по актеру")  

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_all)
        btn_layout.addWidget(self.btn_search)
        btn_layout.addWidget(self.btn_search_by_actor)  

        layout.addLayout(btn_layout)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(lambda: stack.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.add_page = AddSeriesPage(self.stack)
        self.all_page = AllSeriesPage(self.stack)
        self.search_page = SearchSeriesByTitlePage(self.stack)
        self.search_by_actor_page = SearchSeriesByActorPage(self.stack)  

        self.btn_add.clicked.connect(lambda: self.open_page(self.add_page))
        self.btn_all.clicked.connect(lambda: self.open_page(self.all_page))
        self.btn_search.clicked.connect(lambda: self.open_page(self.search_page))
        self.btn_search_by_actor.clicked.connect(lambda: self.open_page(self.search_by_actor_page))  

    def open_page(self, page: QWidget):
        if self.stack.indexOf(page) == -1:
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)