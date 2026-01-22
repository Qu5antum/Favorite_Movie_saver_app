from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from app.service.series_service import get_all_serieses, delete_series_by_id, update_watched_series


class AllSeriesPage(QWidget):
    WATCHED_COL = 3

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Все Сериалы")

        self.current_order = None

        layout = QVBoxLayout(self)

        filter_layout = QHBoxLayout()

        self.btn_all = QPushButton("Все")
        self.btn_old = QPushButton("Старые")
        self.btn_new = QPushButton("Новые")

        self.btn_all.clicked.connect(lambda: self.set_filter(None))
        self.btn_old.clicked.connect(lambda: self.set_filter("asc"))
        self.btn_new.clicked.connect(lambda: self.set_filter("desc"))

        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_old)
        filter_layout.addWidget(self.btn_new)

        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Название Сериала", "Год", "Актёры", "Просмотрен"]
        )

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.itemChanged.connect(self.on_watched_changed)

        layout.addWidget(self.table)

        self.btn_delete = QPushButton("Удалить Сериал")
        layout.addWidget(self.btn_delete)

        self.btn_delete.clicked.connect(self.delete_series)

    def set_filter(self, order: str | None):
        self.current_order = order
        self.load_series()

    def load_series(self):
        serieses = get_all_serieses(self.current_order)

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

            # сохраняем series id
            watched_item.setData(Qt.UserRole, series.id)
            watched_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, self.WATCHED_COL, watched_item)

        self.table.blockSignals(False)  
        self.table.resizeColumnsToContents()

    def on_watched_changed(self, item: QTableWidgetItem):
        if item.column() != self.WATCHED_COL:
            return

        series_id = item.data(Qt.UserRole)
        watched = item.checkState() == Qt.Checked

        update_watched_series(series_id, watched)
    
    def delete_series(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите сериал для удаления"
            )
            return

        item = self.table.item(row, self.WATCHED_COL)
        series_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить выбранный сериал?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        success = delete_series_by_id(series_id)

        if success:
            self.load_series()
        else:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось удалить сериал"
            )

