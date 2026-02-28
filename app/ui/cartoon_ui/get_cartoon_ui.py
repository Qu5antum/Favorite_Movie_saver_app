from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
import webbrowser

from app.database.db import session
from app.service.cartoon_service import CartoonService
from .update_cartoon_ui import UpdateCartoonPage


class AllCartoonPage(QWidget):
    WATCHED_COL = 3
    URL_COL = 4

    def __init__(self, stack):
        super().__init__()

        self.session = session
        self.cartoon_service = CartoonService(session=self.session)

        self.stack = stack
        self.setWindowTitle("Все Мультфильмы")

        self.current_order = None
        self.current_watched = None 

        layout = QVBoxLayout(self)

        filter_layout = QHBoxLayout()
        self.btn_all = QPushButton("Все")
        self.btn_old = QPushButton("Старые")
        self.btn_new = QPushButton("Новые")
        self.btn_watched = QPushButton("Смотрел")
        self.btn_no_watched = QPushButton("Не Смотрел")
        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_old)
        filter_layout.addWidget(self.btn_new)
        filter_layout.addWidget(self.btn_watched)
        filter_layout.addWidget(self.btn_no_watched)

        self.btn_all.clicked.connect(self.reset_filters)
        self.btn_old.clicked.connect(lambda: self.set_filter("asc"))
        self.btn_new.clicked.connect(lambda: self.set_filter("desc"))
        self.btn_watched.clicked.connect(lambda: self.set_watched_filter(True))
        self.btn_no_watched.clicked.connect(lambda: self.set_watched_filter(False))

        layout.addLayout(filter_layout)

        # Кнопка "Назад"
        back_btn = QPushButton("<- Назад")
        back_btn.clicked.connect(self.go_back)

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # добавили колонку для ссылки
        self.table.setHorizontalHeaderLabels(
            ["Название Мультфильма", "Год", "Тип", "Просмотрен", "Ссылка"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemChanged.connect(self.on_watched_changed)
        self.table.cellClicked.connect(self.on_cell_clicked)  # обработка клика по ссылке
        layout.addWidget(self.table)

        # Кнопки
        self.btn_delete = QPushButton("Удалить мультфильм")
        self.btn_update = QPushButton("Редактировать мультфильм")
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_delete)
        self.btn_update.clicked.connect(self.open_update_page)
        self.btn_delete.clicked.connect(self.delete_cartoon)
        layout.addWidget(back_btn)

        self.setLayout(layout)
        self.load_cartoons()

    def go_back(self):
        self.stack.setCurrentIndex(3)

    def load_cartoons(self):
        cartoons = self.cartoon_service.get_all_cartoons(
            watched=self.current_watched,
            order=self.current_order
        )

        self.table.blockSignals(True) 
        self.table.setRowCount(len(cartoons))

        for row, cartoon in enumerate(cartoons):
            self.table.setItem(row, 0, QTableWidgetItem(cartoon.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(cartoon.year)))
            self.table.setItem(row, 2, QTableWidgetItem(cartoon.cartoon_type))
            
            watched_item = QTableWidgetItem()
            watched_item.setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
            )
            watched_item.setCheckState(Qt.Checked if cartoon.watched else Qt.Unchecked)
            watched_item.setData(Qt.UserRole, cartoon.id)
            watched_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.WATCHED_COL, watched_item)

            url_item = QTableWidgetItem(cartoon.url or "")
            url_item.setForeground(Qt.blue)
            url_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            url_item.setData(Qt.UserRole, cartoon.url)
            self.table.setItem(row, self.URL_COL, url_item)

        self.table.blockSignals(False)
        self.table.resizeColumnsToContents()

    def on_watched_changed(self, item: QTableWidgetItem):
        if item.column() != self.WATCHED_COL:
            return
        cartoon_id = item.data(Qt.UserRole)
        watched = item.checkState() == Qt.Checked
        self.cartoon_service.update_watched_cartoon(cartoon_id, watched)

    def on_cell_clicked(self, row, column):
        if column == self.URL_COL:
            url_item = self.table.item(row, column)
            url = url_item.data(Qt.UserRole)
            if url:
                webbrowser.open(url)

    def open_update_page(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите мультфильм")
            return
        item = self.table.item(row, self.WATCHED_COL)
        cartoon_id = item.data(Qt.UserRole)
        self.update_window = UpdateCartoonPage(self.stack, cartoon_id)
        self.update_window.destroyed.connect(self.load_cartoons)
        self.update_window.show()

    def reset_filters(self):
        self.current_order = None
        self.current_watched = None
        self.load_cartoons()

    def set_watched_filter(self, watched: bool | None):
        self.current_watched = watched
        self.load_cartoons()

    def set_filter(self, order: str | None):
        self.current_order = order
        self.load_cartoons()

    def delete_cartoon(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите мультфильм для удаления")
            return
        item = self.table.item(row, self.WATCHED_COL)
        cartoon_id = item.data(Qt.UserRole)
        reply = QMessageBox.question(
            self, "Подтверждение", "Удалить выбранный мультфильм?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        success = self.cartoon_service.delete_cartoon_by_id(cartoon_id)
        if success:
            self.load_cartoons()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить мультфильм")