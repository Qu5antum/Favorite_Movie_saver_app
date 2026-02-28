from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QMessageBox
)
from app.database.db import session
from app.service.cartoon_service import CartoonService


class UpdateCartoonPage(QWidget):
    def __init__(self, stack, cartoon_id: int):
        super().__init__()
        self.stack = stack
        self.cartoon_id = cartoon_id

        # рабочая сессия и сервис
        self.session = session
        self.cartoon_service = CartoonService(session=self.session)

        self.setWindowTitle("Редактировать мультфильм")
        layout = QVBoxLayout()

        # Поля для редактирования
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название мультфильма")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Тип мультфильма")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ссылка (если есть)")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        # Кнопка сохранить изменения
        self.save_btn = QPushButton("Сохранить изменения")
        self.save_btn.clicked.connect(self.update_movie)

        layout.addWidget(self.title_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.type_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.url_input)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # загружаем данные мультфильма
        self.load_cartoon()

    def load_cartoon(self):
        cartoon = self.cartoon_service.get_cartoon_by_id(self.cartoon_id)

        if not cartoon:
            QMessageBox.warning(self, "Ошибка", "Мультфильм не найден")
            return

        self.title_input.setText(cartoon.title or "")
        self.year_input.setText(str(cartoon.year) if cartoon.year else "")
        self.type_input.setText(cartoon.cartoon_type or "")
        self.desc_input.setPlainText(cartoon.description or "")
        self.url_input.setText(cartoon.url or "")

    def update_movie(self):
        title = self.title_input.text().strip()
        year_text = self.year_input.text().strip()
        year = int(year_text) if year_text.isdigit() else None
        cartoon_type = self.type_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        url = self.url_input.text().strip()

        # вызываем метод сервиса для обновления
        success = self.cartoon_service.update_cartoon(
            cartoon_id=self.cartoon_id,
            title=title if title else None,
            year=year,
            description=description if description else None,
            cartoon_type=cartoon_type if cartoon_type else None,
            url=url if url else None
        )

        if success:
            QMessageBox.information(self, "Успех", "Изменения сохранены!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить мультфильм")