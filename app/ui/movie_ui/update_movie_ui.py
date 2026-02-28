from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QMessageBox
)

from app.database.db import session
from app.service.movie_service import MovieService


class UpdateMoviePage(QWidget):
    def __init__(self, stack, movie_id: int):
        super().__init__()

        self.stack = stack
        self.movie_id = movie_id

        self.session = session
        self.movie_service = MovieService(session=self.session)

        self.setWindowTitle("Редактировать фильм")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название фильма")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        self.actors_input = QLineEdit()
        self.actors_input.setPlaceholderText("Актеры (через запятую ОБЯЗАТЕЛЬНО!!!)")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ссылка")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        self.save_btn = QPushButton("Сохранить изменения")
        self.save_btn.clicked.connect(self.update_movie)

        layout.addWidget(self.title_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.actors_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.url_input)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.load_movie()

    def load_movie(self):
        movie = self.movie_service.get_movie_by_id(self.movie_id)

        if not movie:
            QMessageBox.warning(self, "Ошибка", "Фильм не найден")
            return

        self.title_input.setText(movie.title or "")
        self.year_input.setText(str(movie.year) if movie.year else "")
        self.desc_input.setPlainText(movie.description or "")
        self.url_input.setText(movie.url or "")

        actors = ", ".join(a.name for a in movie.movie_actors)
        self.actors_input.setText(actors)

    def update_movie(self):
        title = self.title_input.text().strip()
        year_text = self.year_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        url = self.url_input.text().strip()

        year = int(year_text) if year_text.isdigit() else None

        actor_list = [
            a.strip() for a in self.actors_input.text().split(",") if a.strip()
        ] 
        
        success = self.movie_service.update_movie(
            movie_id=self.movie_id,
            title=title if title else None,
            year=year,
            description=description if description else None,
            url=url if url else None,
            actor_list=actor_list
        )

        if success:
            QMessageBox.information(self, "Успех", "Фильм обновлён!")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить фильм")