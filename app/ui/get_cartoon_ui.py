from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from app.service.cartoon_service import get_all_cartoons, update_watched_cartoon, delete_cartoon_by_id


class AllCartoonPage(QWidget):
    WATCHED_COL = 3

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Все Мультфильмы")

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
            ["Название Мультфильма", "Год", "Тип", "Просмотрен"]
        )

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.itemChanged.connect(self.on_watched_changed)

        layout.addWidget(self.table)

        self.btn_delete = QPushButton("Удалить фильм")
        layout.addWidget(self.btn_delete)

        self.btn_delete.clicked.connect(self.delete_cartoon)

    def set_filter(self, order: str | None):
        self.current_order = order
        self.load_cartoons()

    def load_cartoons(self):
        cartoons = get_all_cartoons(self.current_order)

        self.table.blockSignals(True) 
        self.table.setRowCount(len(cartoons))

        for row, cartoon in enumerate(cartoons):
            self.table.setItem(row, 0, QTableWidgetItem(cartoon.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(cartoon.year)))
            self.table.setItem(row, 2, QTableWidgetItem(cartoon.cartoon_type))
        
            watched_item = QTableWidgetItem()
            watched_item.setFlags(
                Qt.ItemIsSelectable |
                Qt.ItemIsEnabled |
                Qt.ItemIsUserCheckable
            )
            watched_item.setCheckState(
                Qt.Checked if cartoon.watched else Qt.Unchecked
            )

            watched_item.setData(Qt.UserRole, cartoon.id)
            watched_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, self.WATCHED_COL, watched_item)

        self.table.blockSignals(False)  
        self.table.resizeColumnsToContents()

    def on_watched_changed(self, item: QTableWidgetItem):
        if item.column() != self.WATCHED_COL:
            return

        cartoon_id = item.data(Qt.UserRole)
        watched = item.checkState() == Qt.Checked

        update_watched_cartoon(cartoon_id, watched)
    
    def delete_cartoon(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите мультфальм для удаления"
            )
            return

        item = self.table.item(row, self.WATCHED_COL)
        cartoon_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить выбранный мультфильм?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        success = delete_cartoon_by_id(cartoon_id)

        if success:
            self.load_cartoons()
        else:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось удалить мультфильм"
            )

