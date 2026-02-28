from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QCheckBox, QMessageBox
)
from app.service.cartoon_service import CartoonService
from app.database.db import session

class AddCartoonPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.session = session
        self.cartoon_service = CartoonService(session=self.session)

        self.stack = stack
        self.setWindowTitle("Добавить Мультфильм")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название Мультифильма")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Тип мультфильма(Полнометражный или Мультсериал)")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ссылка (если есть)")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        self.watched_checkbox = QCheckBox("Смотрел?")

        self.save_btn = QPushButton("Добавить")
        self.save_btn.clicked.connect(self.save_movie)

        layout.addWidget(self.title_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.type_input)
        layout.addWidget(self.url_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.watched_checkbox)
        layout.addWidget(self.save_btn)

        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def go_back(self):
        self.stack.setCurrentIndex(3)

    def save_movie(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Error", "Требуется название")
            return

        year_text = self.year_input.text().strip()
        year = int(year_text) if year_text.isdigit() else None
        url = self.url_input.text().strip() or None

        
        self.cartoon_service.add_cartoon(
            title=title,
            year=year,
            cartoon_type=self.type_input.text(),
            description=self.desc_input.toPlainText(),
            watched=self.watched_checkbox.isChecked(),
            url=url
        )

        QMessageBox.information(self, "Success", "Мультфильм добавлен!")

        self.title_input.clear()
        self.year_input.clear()
        self.type_input.clear()
        self.desc_input.clear()
        self.watched_checkbox.setChecked(False)
