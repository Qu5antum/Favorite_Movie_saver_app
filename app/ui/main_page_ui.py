from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QPushButton, QVBoxLayout,
    QStackedWidget, QLabel
)
from PySide6.QtGui import QIcon
import sys

from .cartoon_ui.cartoon_page_ui import CartoonPage
from .movie_ui.movie_page_ui import MoviesPage
from .series_ui.series_page_ui import SeriesPage

#Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Фильмотека")
        self.setWindowIcon(QIcon("app/assets/favicon.ico"))
        self.resize(1200, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # страницы
        self.main_page = QWidget()
        self.movies_page = MoviesPage(self.stack)
        self.series_page = SeriesPage(self.stack)
        self.cartoon_page = CartoonPage(self.stack)

        self.stack.addWidget(self.main_page)     
        self.stack.addWidget(self.movies_page)   
        self.stack.addWidget(self.series_page)   
        self.stack.addWidget(self.cartoon_page)  

        self.init_main_page()

    def init_main_page(self):
        layout = QVBoxLayout()

        btn_movies = QPushButton("🎬 Фильмы")
        btn_series = QPushButton("📺 Сериалы")
        btn_cartoon = QPushButton("🧸 Мультфильмы")
        btn_movies.setFixedSize(1200, 200)
        btn_series.setFixedSize(1200, 200)
        btn_cartoon.setFixedSize(1200, 200)
        btn_movies.setStyleSheet("font-size: 24px;")
        btn_series.setStyleSheet("font-size: 24px;")
        btn_cartoon.setStyleSheet("font-size: 24px;")

    
        btn_movies.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_series.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_cartoon.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        layout.addWidget(btn_movies)
        layout.addWidget(btn_series)
        layout.addWidget(btn_cartoon)

        self.main_page.setLayout(layout)

