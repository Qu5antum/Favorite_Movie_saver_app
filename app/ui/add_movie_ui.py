from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QCheckBox, QMessageBox
)
from app.service.movie_service import add_new_movie


class AddMoviePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить Фильм")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название Фильма")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        self.actors_input = QLineEdit()
        self.actors_input.setPlaceholderText("Актеры (через запятую ОБЯЗАТЕЛЬНО!!!)")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        self.watched_checkbox = QCheckBox("Смотрел?")

        self.save_btn = QPushButton("Добавить")
        self.save_btn.clicked.connect(self.save_movie)

        layout.addWidget(self.title_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.actors_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.watched_checkbox)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_movie(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Error", "Требуется название")
            return

        year_text = self.year_input.text().strip()
        year = int(year_text) if year_text.isdigit() else None

        actors = [
            a.strip() for a in self.actors_input.text().split(",") if a.strip()
        ]

        add_new_movie(
            title=title,
            year=year,
            description=self.desc_input.toPlainText(),
            watched=self.watched_checkbox.isChecked(),
            actors=actors,
        )

        QMessageBox.information(self, "Success", "Фильм добавлен!")

        self.title_input.clear()
        self.year_input.clear()
        self.actors_input.clear()
        self.desc_input.clear()
        self.watched_checkbox.setChecked(False)
