from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PySide6.QtGui import QIcon

from .add_movie_ui import AddMoviePage
from .get_movies_ui import AllMoviesPage
from .search_movie_ui import SearchMovieByTitlePage
from .filter_movies_ui import SearchMovieByActorPage  

class MoviesPage(QWidget):
    def __init__(self, stack: QStackedWidget):
        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        layout.addWidget(QLabel("🎬 Страница фильмов"))

        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ Добавить фильм")
        self.btn_all = QPushButton("📄 Все фильмы")
        self.btn_search = QPushButton("🔍 Поиск фильмов")
        self.btn_search_by_actor = QPushButton("🎭 Поиск по актеру")  
        self.btn_add.setFixedSize(300, 600)
        self.btn_all.setFixedSize(300, 600)
        self.btn_search.setFixedSize(300, 600)
        self.btn_search_by_actor.setFixedSize(300, 600)
        self.btn_add.setStyleSheet("font-size: 24px;")
        self.btn_all.setStyleSheet("font-size: 24px;")
        self.btn_search.setStyleSheet("font-size: 24px;")
        self.btn_search_by_actor.setStyleSheet("font-size: 24px;")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_all)
        btn_layout.addWidget(self.btn_search)
        btn_layout.addWidget(self.btn_search_by_actor)  

        layout.addLayout(btn_layout)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(lambda: stack.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.add_page = AddMoviePage(self.stack)
        self.all_page = AllMoviesPage(self.stack)
        self.search_page = SearchMovieByTitlePage(self.stack)
        self.search_by_actor_page = SearchMovieByActorPage(self.stack)  

        self.btn_add.clicked.connect(lambda: self.open_page(self.add_page))
        self.btn_all.clicked.connect(lambda: self.open_page(self.all_page))
        self.btn_search.clicked.connect(lambda: self.open_page(self.search_page))
        self.btn_search_by_actor.clicked.connect(lambda: self.open_page(self.search_by_actor_page))  

    def open_page(self, page: QWidget):
        if self.stack.indexOf(page) == -1:
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)