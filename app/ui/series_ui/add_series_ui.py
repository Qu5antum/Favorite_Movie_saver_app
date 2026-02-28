from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QCheckBox, QMessageBox
)
from app.database.db import session
from app.service.series_service import SeriesService

class AddSeriesPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Добавить Сериал")

        self.session = session
        self.series_service = SeriesService(session=session)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название Сериала")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        self.actors_input = QLineEdit()
        self.actors_input.setPlaceholderText("Актеры (через запятую ОБЯЗАТЕЛЬНО!!!)")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ссылка (если есть)")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        self.watched_checkbox = QCheckBox("Смотрел?")

        self.save_btn = QPushButton("Добавить")
        self.save_btn.clicked.connect(self.save_series)

        layout.addWidget(self.title_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.actors_input)
        layout.addWidget(self.url_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.watched_checkbox)
        layout.addWidget(self.save_btn)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def go_back(self):
        self.stack.setCurrentIndex(2)  

    def save_series(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Error", "Требуется название")
            return

        year_text = self.year_input.text().strip()
        year = int(year_text) if year_text.isdigit() else None

        actors = [
            a.strip() for a in self.actors_input.text().split(",") if a.strip()
        ]

        url = self.url_input.text().strip() or None

        self.series_service.add_series(
            title=title,
            year=year,
            description=self.desc_input.toPlainText(),
            watched=self.watched_checkbox.isChecked(),
            actors=actors,
            url=url
        )

        QMessageBox.information(self, "Success", "Сериал добавлен!")

        self.title_input.clear()
        self.year_input.clear()
        self.actors_input.clear()
        self.url_input.clear()
        self.desc_input.clear()
        self.watched_checkbox.setChecked(False)