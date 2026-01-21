from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QCheckBox, QMessageBox
)
from app.service.cartoon_service import add_cartoon


class AddCartoonPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить Мультфильм")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название Мультифильма")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Тип мультфильма(Полнометражный или Мультсериал)")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        self.watched_checkbox = QCheckBox("Смотрел?")

        self.save_btn = QPushButton("Добавить")
        self.save_btn.clicked.connect(self.save_movie)

        layout.addWidget(self.title_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.type_input)
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

        
        add_cartoon(
            title=title,
            year=year,
            cartoon_type=self.type_input.text(),
            description=self.desc_input.toPlainText(),
            watched=self.watched_checkbox.isChecked(),
        )

        QMessageBox.information(self, "Success", "Мультфильм добавлен!")

        self.title_input.clear()
        self.year_input.clear()
        self.type_input.clear()
        self.desc_input.clear()
        self.watched_checkbox.setChecked(False)
