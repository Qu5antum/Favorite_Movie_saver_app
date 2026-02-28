from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QMessageBox
)

from app.database.db import session
from app.service.series_service import SeriesService


class UpdateSeriesPage(QWidget):
    def __init__(self, stack, series_id: int):
        super().__init__()

        self.stack = stack
        self.series_id = series_id

        self.session = session
        self.series_service = SeriesService(session=self.session)

        self.setWindowTitle("Редактировать сериал")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название сериала")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        self.actors_input = QLineEdit()
        self.actors_input.setPlaceholderText("Актеры (через запятую ОБЯЗАТЕЛЬНО!!!)")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ссылка")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        self.save_btn = QPushButton("Сохранить изменения")
        self.save_btn.clicked.connect(self.update_series)

        layout.addWidget(self.title_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.actors_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.url_input)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.load_series()

    def load_series(self):
        series = self.series_service.get_series_by_id(self.series_id)

        if not series:
            QMessageBox.warning(self, "Ошибка", "Сериал не найден")
            return

        self.title_input.setText(series.title or "")
        self.year_input.setText(str(series.year) if series.year else "")
        self.desc_input.setPlainText(series.description or "")
        self.url_input.setText(series.url or "")

        actors = ", ".join(a.name for a in series.series_actors)
        self.actors_input.setText(actors)

    def update_series(self):
        title = self.title_input.text().strip()
        year_text = self.year_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        url = self.url_input.text().strip()

        year = int(year_text) if year_text.isdigit() else None

        actor_list = [
            a.strip() for a in self.actors_input.text().split(",") if a.strip()
        ] 
        
        success = self.series_service.update_series(
            series_id=self.series_id,
            title=title if title else None,
            year=year,
            description=description if description else None,
            url=url if url else None,
            actor_list=actor_list
        )

        if success:
            QMessageBox.information(self, "Успех", "Сериал обновлён!")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить сериал")