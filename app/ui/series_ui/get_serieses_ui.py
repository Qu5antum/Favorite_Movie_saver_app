from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
import webbrowser

from app.database.db import session
from app.service.series_service import SeriesService


class AllSeriesPage(QWidget):
    WATCHED_COL = 3
    URL_COL = 4 

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Все Сериалы")

        self.session = session
        self.series_service = SeriesService(session=session)

        self.current_order = None
        self.current_watched = None 

        layout = QVBoxLayout(self)

        filter_layout = QHBoxLayout()

        self.btn_all = QPushButton("Все")
        self.btn_old = QPushButton("Старые")
        self.btn_new = QPushButton("Новые")
        self.btn_watched = QPushButton("Смотрел")
        self.btn_no_watched = QPushButton("Не Смотрел")

        self.btn_all.clicked.connect(self.reset_filters)
        self.btn_old.clicked.connect(lambda: self.set_filter("asc"))
        self.btn_new.clicked.connect(lambda: self.set_filter("desc"))
        self.btn_watched.clicked.connect(lambda: self.set_watched_filter(True))
        self.btn_no_watched.clicked.connect(lambda: self.set_watched_filter(False))

        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_old)
        filter_layout.addWidget(self.btn_new)
        filter_layout.addWidget(self.btn_watched)
        filter_layout.addWidget(self.btn_no_watched)

        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Название Сериала", "Год", "Актёры", "Просмотрен", "Ссылка"]
        )

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemChanged.connect(self.on_watched_changed)
        self.table.cellClicked.connect(self.open_url_from_cell)

        layout.addWidget(self.table)

        # Кнопка Назад
        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)

        self.btn_delete = QPushButton("Удалить Сериал")
        layout.addWidget(self.btn_delete)
        self.btn_delete.clicked.connect(self.delete_series)
        layout.addWidget(back_btn)

    def go_back(self):
        self.stack.setCurrentIndex(2) 

    def reset_filters(self):
        self.current_order = None
        self.current_watched = None
        self.load_series()

    def set_watched_filter(self, watched: bool | None):
        self.current_watched = watched
        self.load_series()

    def set_filter(self, order: str | None):
        self.current_order = order
        self.load_series()

    def load_series(self):
        serieses = self.series_service.get_all_serieses(
            watched=self.current_watched,
            order=self.current_order
        )

        self.table.blockSignals(True)
        self.table.setRowCount(len(serieses))

        for row, series in enumerate(serieses):
            self.table.setItem(row, 0, QTableWidgetItem(series.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(series.year)))
            self.table.setItem(
                row, 2,
                QTableWidgetItem(", ".join(a.name for a in series.series_actors))
            )

            watched_item = QTableWidgetItem()
            watched_item.setFlags(
                Qt.ItemIsSelectable |
                Qt.ItemIsEnabled |
                Qt.ItemIsUserCheckable
            )
            watched_item.setCheckState(
                Qt.Checked if series.watched else Qt.Unchecked
            )
            watched_item.setData(Qt.UserRole, series.id)
            watched_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.WATCHED_COL, watched_item)

            # Колонка URL
            url_item = QTableWidgetItem(series.url or "")
            url_item.setTextAlignment(Qt.AlignCenter)
            url_item.setForeground(Qt.blue)
            self.table.setItem(row, self.URL_COL, url_item)

        self.table.blockSignals(False)
        self.table.resizeColumnsToContents()

    def on_watched_changed(self, item: QTableWidgetItem):
        if item.column() != self.WATCHED_COL:
            return
        series_id = item.data(Qt.UserRole)
        watched = item.checkState() == Qt.Checked
        self.series_service.update_watched_series(series_id, watched)

    def delete_series(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сериал для удаления")
            return

        item = self.table.item(row, self.WATCHED_COL)
        series_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self, "Подтверждение", "Удалить выбранный сериал?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.No:
            return

        success = self.series_service.delete_series_by_id(series_id)
        if success:
            self.load_series()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить сериал")

    def open_url_from_cell(self, row, column):
        if column == self.URL_COL:
            url_item = self.table.item(row, column)
            url = url_item.text().strip()
            if url:
                import webbrowser
                webbrowser.open(url)
            else:
                QMessageBox.information(self, "Информация", "Ссылка отсутствует")