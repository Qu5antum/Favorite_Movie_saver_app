from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QStackedWidget, QHBoxLayout
)

from app.ui.add_movie_ui import AddMoviePage
from app.ui.add_series_ui import AddSeriesPage
from app.ui.get_movies_ui import AllMoviesPage
from app.ui.get_serieses_ui import AllSeriesPage
from app.ui.filter_movies_ui import SearchByActorPage
from app.ui.search_movie_ui import SearchMovieByTitlePage
from app.ui.search_series_iu import SearchSeriesByTitlePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Мои фильмы")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        sidebar = QVBoxLayout()
        btn_movies = QPushButton("Все Фильмы")
        btn_serieses = QPushButton("Все Сериалы")
        btn_add_movie = QPushButton("Добавить Фильм")
        btn_add_series = QPushButton("Добавить Сериал")
        btn_search_movie_title = QPushButton("Поиск Фильма по названию")
        btn_search_series_title = QPushButton("Поиск Сериала по названию")
        btn_search_actor = QPushButton("Поиск Фильма по актёру")

        sidebar.addWidget(btn_movies)
        sidebar.addWidget(btn_serieses)
        sidebar.addWidget(btn_add_movie)
        sidebar.addWidget(btn_add_series)
        sidebar.addWidget(btn_search_movie_title)
        sidebar.addWidget(btn_search_series_title)
        sidebar.addWidget(btn_search_actor)
        sidebar.addStretch()

        self.stack = QStackedWidget()

        self.page_movies = AllMoviesPage()
        self.page_serieses = AllSeriesPage()
        self.page_add_film = AddMoviePage()
        self.page_add_series = AddSeriesPage()
        self.page_search_movie_title = SearchMovieByTitlePage()
        self.page_search_series_title = SearchSeriesByTitlePage()
        self.page_search_actor = SearchByActorPage()

        self.stack.addWidget(self.page_movies)  
        self.stack.addWidget(self.page_serieses)
        self.stack.addWidget(self.page_add_film)  
        self.stack.addWidget(self.page_add_series)
        self.stack.addWidget(self.page_search_movie_title) 
        self.stack.addWidget(self.page_search_series_title)
        self.stack.addWidget(self.page_search_actor)   

       
        btn_movies.clicked.connect(self.open_movies)
        btn_serieses.clicked.connect(self.open_serieses)
        btn_add_movie.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_add_series.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_add_series))
        btn_search_movie_title.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_movie_title)
        )

        btn_search_series_title.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_series_title)
        )

        btn_search_actor.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_actor)
        )


      
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)

     
        self.open_movies()
        self.open_serieses

    def open_movies(self):
        self.page_movies.load_movies()
        self.stack.setCurrentIndex(0)

    def open_serieses(self):
        self.page_serieses.load_series()
        self.stack.setCurrentIndex(1)
