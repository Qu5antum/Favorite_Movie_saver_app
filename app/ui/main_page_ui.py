from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QStackedWidget, QHBoxLayout
)

from app.ui.add_movie_ui import AddMoviePage
from app.ui.get_movies_ui import AllMoviesPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Мои фильмы")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # 🔹 Sidebar
        sidebar = QVBoxLayout()
        btn_movies = QPushButton("Все фильмы")
        btn_add = QPushButton("Добавить фильм")

        sidebar.addWidget(btn_movies)
        sidebar.addWidget(btn_add)
        sidebar.addStretch()

        # 🔹 Pages
        self.stack = QStackedWidget()

        self.page_movies = AllMoviesPage()
        self.page_add = AddMoviePage()

        self.stack.addWidget(self.page_movies)  # index 0
        self.stack.addWidget(self.page_add)     # index 1

        # 🔹 Navigation
        btn_movies.clicked.connect(self.open_movies)
        btn_add.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        # 🔹 Layout
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)

        # 🔹 Start page
        self.open_movies()

    def open_movies(self):
        self.page_movies.load_movies()
        self.stack.setCurrentIndex(0)
