from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QStackedWidget, QHBoxLayout
)

from app.ui.add_movie_ui import AddMoviePage
from app.ui.get_movies_ui import AllMoviesPage
from app.ui.filter_movies_ui import SearchByActorPage
from app.ui.search_movie_ui import SearchByTitlePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Мои фильмы")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        sidebar = QVBoxLayout()
        btn_movies = QPushButton("Все фильмы")
        btn_add = QPushButton("Добавить фильм")
        btn_search_title = QPushButton("Поиск по названию")
        btn_search_actor = QPushButton("Поиск по актёру")

        sidebar.addWidget(btn_movies)
        sidebar.addWidget(btn_add)
        sidebar.addWidget(btn_search_title)
        sidebar.addWidget(btn_search_actor)
        sidebar.addStretch()

        self.stack = QStackedWidget()

        self.page_movies = AllMoviesPage()
        self.page_add = AddMoviePage()
        self.page_search_title = SearchByTitlePage()
        self.page_search_actor = SearchByActorPage()

        self.stack.addWidget(self.page_movies)  
        self.stack.addWidget(self.page_add)  
        self.stack.addWidget(self.page_search_title) 
        self.stack.addWidget(self.page_search_actor)   

       
        btn_movies.clicked.connect(self.open_movies)
        btn_add.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_search_title.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_title)
        )

        btn_search_actor.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_search_actor)
        )


      
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)

     
        self.open_movies()

    def open_movies(self):
        self.page_movies.load_movies()
        self.stack.setCurrentIndex(0)
