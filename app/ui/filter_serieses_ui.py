from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt

from app.service.series_service import filter_serieses_by_actor


class SearchSeriesByActorPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите имя актёра из сериала")
        self.btn_search = QPushButton("Поиск")

        search_layout.addWidget(self.input)
        search_layout.addWidget(self.btn_search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Название Сериала", "Год", "Актёры", "Просмотрен"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)

        self.btn_search.clicked.connect(self.search)

    def search(self):
        actor_name = self.input.text().strip()
        if not actor_name:
            return

        serieses = filter_serieses_by_actor(actor_name)

        self.table.setRowCount(len(serieses))

        for row, series in enumerate(serieses):
            self.table.setItem(row, 0, QTableWidgetItem(series.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(series.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in series.series_actors))
            )

            watched = QTableWidgetItem("✔" if series.watched else "—")
            watched.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, watched)

        self.table.resizeColumnsToContents()
