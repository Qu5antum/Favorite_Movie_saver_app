from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QStackedWidget, QHBoxLayout
)
from PySide6.QtGui import QIcon

from app.ui.add_movie_ui import AddMoviePage
from app.ui.add_series_ui import AddSeriesPage
from app.ui.get_movies_ui import AllMoviesPage
from app.ui.get_serieses_ui import AllSeriesPage
from app.ui.search_movie_ui import SearchMovieByTitlePage
from app.ui.search_series_iu import SearchSeriesByTitlePage
from app.ui.filter_movies_ui import SearcMoviehByActorPage
from app.ui.filter_serieses_ui import SearchSeriesByActorPage

#Cartoon
from app.ui.add_cartoon_ui import AddCartoonPage
from app.ui.get_cartoon_ui import AllCartoonPage
from app.ui.search_cartoon import SearchCartoonByTitlePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Фильмотека")
        self.setWindowIcon(QIcon("app/assets/logo.webp")) 
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # ---------- Sidebar ----------
        sidebar = QVBoxLayout()

        btn_movies = QPushButton("Все Фильмы")
        btn_serieses = QPushButton("Все Сериалы")
        btn_add_movie = QPushButton("Добавить Фильм")
        btn_add_series = QPushButton("Добавить Сериал")
        btn_search_movie_title = QPushButton("Поиск Фильма по названию")
        btn_search_series_title = QPushButton("Поиск Сериала по названию")
        btn_search_movie_actor = QPushButton("Поиск Фильма по актёру")
        btn_search_series_actor = QPushButton("Поиск Сериала по актёру")
        btn_add_cartoon = QPushButton("Добавить Мультфильм")
        btn_cartoons = QPushButton("Все Мультфильмы")
        btn_search_cartoon_title = QPushButton("Поиск мультфильма по названию")

        sidebar.addWidget(btn_movies)
        sidebar.addWidget(btn_serieses)
        sidebar.addWidget(btn_add_movie)
        sidebar.addWidget(btn_add_series)
        sidebar.addWidget(btn_search_movie_title)
        sidebar.addWidget(btn_search_series_title)
        sidebar.addWidget(btn_search_movie_actor)
        sidebar.addWidget(btn_search_series_actor)
        sidebar.addWidget(btn_add_cartoon)
        sidebar.addWidget(btn_cartoons)
        sidebar.addWidget(btn_search_cartoon_title)
        sidebar.addStretch()

        # ---------- Pages ----------
        self.stack = QStackedWidget()

        self.page_movies = AllMoviesPage()
        self.page_serieses = AllSeriesPage()
        self.page_add_film = AddMoviePage()
        self.page_add_series = AddSeriesPage()
        self.page_search_movie_title = SearchMovieByTitlePage()
        self.page_search_series_title = SearchSeriesByTitlePage()
        self.page_search_movie_actor = SearcMoviehByActorPage()
        self.page_search_series_actor = SearchSeriesByActorPage()
        self.page_add_cartoon = AddCartoonPage()
        self.page_cartoons = AllCartoonPage()
        self.page_search_cartoon = SearchCartoonByTitlePage()

        self.stack.addWidget(self.page_movies)
        self.stack.addWidget(self.page_serieses)
        self.stack.addWidget(self.page_add_film)
        self.stack.addWidget(self.page_add_series)
        self.stack.addWidget(self.page_search_movie_title)
        self.stack.addWidget(self.page_search_series_title)
        self.stack.addWidget(self.page_search_movie_actor)
        self.stack.addWidget(self.page_search_series_actor)
        self.stack.addWidget(self.page_add_cartoon)
        self.stack.addWidget(self.page_cartoons)
        self.stack.addWidget(self.page_search_cartoon)

        # ---------- Connections ----------
        btn_movies.clicked.connect(self.open_movies)
        btn_serieses.clicked.connect(self.open_serieses)
        btn_cartoons.clicked.connect(self.open_cartoons)

        btn_add_movie.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_add_film)
        )
        btn_add_series.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_add_series)
        )
        btn_add_cartoon.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_add_cartoon)
        )

        btn_search_movie_title.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_movie_title)
        )
        btn_search_series_title.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_series_title)
        )
        btn_search_movie_actor.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_movie_actor)
        )
        btn_search_series_actor.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_series_actor)
        )
        btn_search_cartoon_title.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_cartoon)
        )

        # ---------- Layout ----------
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)

        # ---------- Start page ----------
        self.open_movies()

    # ---------- Navigation ----------
    def open_movies(self):
        self.page_movies.load_movies()
        self.stack.setCurrentWidget(self.page_movies)

    def open_serieses(self):
        self.page_serieses.load_series()
        self.stack.setCurrentWidget(self.page_serieses)

    def open_cartoons(self):
        self.page_cartoons.load_cartoons()
        self.stack.setCurrentWidget(self.page_cartoons)