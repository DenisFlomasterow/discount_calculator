import csv
import logging

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QDoubleSpinBox, QListWidget, QTableWidget,
    QHeaderView, QGroupBox, QFrame, QMessageBox, QFileDialog,
    QTableWidgetItem
)
from PIL import Image

from database import DatabaseManager
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор скидок")
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)
        self.final_price = None
        self.saved = None
        self.image_path = ""

        central = QWidget()
        self.setCentralWidget(central)

        self._setup_ui()
        self._apply_styles()
        self._bind_signals()
        self._init_db()

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        self.centralWidget().setLayout(main_layout)

        self.lbl_title = QLabel("Калькулятор скидок")
        self.lbl_title.setObjectName("title")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_title)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)
        main_layout.addLayout(content_layout, 1)

        photo_card = QFrame()
        photo_card.setObjectName("card")
        photo_layout = QVBoxLayout(photo_card)

        self.lbl_photo = QLabel("Фото товара")
        self.lbl_photo.setAlignment(Qt.AlignCenter)
        self.lbl_photo.setStyleSheet("border: 2px dashed #aaaaaa; color: #555555;")
        photo_layout.addWidget(self.lbl_photo, 1)

        self.btn_load_photo = QPushButton("Загрузить фото")
        photo_layout.addWidget(self.btn_load_photo)

        content_layout.addWidget(photo_card, 1)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        content_layout.addLayout(right_layout, 1)

        input_card = QFrame()
        input_card.setObjectName("card")
        input_layout = QVBoxLayout(input_card)

        form_layout = QFormLayout()

        self.spin_price = QDoubleSpinBox()
        self.spin_price.setRange(0.01, 1000000.0)
        self.spin_price.setDecimals(2)
        self.spin_price.setValue(1000.0)

        self.spin_discount = QDoubleSpinBox()
        self.spin_discount.setRange(0.0, 100.0)
        self.spin_discount.setDecimals(1)

        self.spin_tax = QDoubleSpinBox()
        self.spin_tax.setRange(0.0, 100.0)
        self.spin_tax.setDecimals(1)

        form_layout.addRow("Цена, руб.", self.spin_price)
        form_layout.addRow("Скидка, %", self.spin_discount)
        form_layout.addRow("Налог, %", self.spin_tax)
        input_layout.addLayout(form_layout)

        self.list_discounts = QListWidget()
        self.list_discounts.setMaximumHeight(70)
        input_layout.addWidget(self.list_discounts)

        list_btn_layout = QHBoxLayout()
        self.btn_add_discount = QPushButton("Добавить скидку")
        self.btn_remove_discount = QPushButton("Удалить")
        self.btn_clear_discounts = QPushButton("Очистить")
        list_btn_layout.addWidget(self.btn_add_discount)
        list_btn_layout.addWidget(self.btn_remove_discount)
        list_btn_layout.addWidget(self.btn_clear_discounts)
        input_layout.addLayout(list_btn_layout)

        self.btn_calculate = QPushButton("Рассчитать")
        self.btn_calculate.setObjectName("accent")
        input_layout.addWidget(self.btn_calculate)

        right_layout.addWidget(input_card)

        result_card = QFrame()
        result_card.setObjectName("card")
        result_layout = QVBoxLayout(result_card)

        lbl_res = QLabel("Итоговая цена:")
        lbl_res.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(lbl_res)

        self.lbl_final_price = QLabel("0")
        self.lbl_final_price.setObjectName("result_number")
        self.lbl_final_price.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.lbl_final_price)

        self.lbl_saved = QLabel("Экономия: 0 руб.")
        self.lbl_saved.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.lbl_saved)

        right_layout.addWidget(result_card, 1)

        history_group = QGroupBox("История расчётов")
        history_layout = QVBoxLayout(history_group)

        self.table_history = QTableWidget()
        self.table_history.setColumnCount(5)
        self.table_history.setHorizontalHeaderLabels(
            ["Цена", "Скидки", "Налог", "Итог", "Экономия"]
        )
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_history.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_history.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_history.setMaximumHeight(160)
        history_layout.addWidget(self.table_history)

        history_btn_layout = QHBoxLayout()
        self.btn_save_history = QPushButton("Сохранить")
        self.btn_update_history = QPushButton("Обновить")
        self.btn_delete_history = QPushButton("Удалить")
        self.btn_export_csv = QPushButton("Экспорт CSV")
        history_btn_layout.addWidget(self.btn_save_history)
        history_btn_layout.addWidget(self.btn_update_history)
        history_btn_layout.addWidget(self.btn_delete_history)
        history_btn_layout.addWidget(self.btn_export_csv)
        history_layout.addLayout(history_btn_layout)

        main_layout.addWidget(history_group)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_status)
    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            #title {
                font-size: 22px;
                font-weight: bold;
                padding: 6px;
            }
            #card {
                background-color: white;
                border-radius: 10px;
            }
            #accent {
                background-color: #4285f4;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
            }
            #accent:hover {
                background-color: #3367d6;
            }
            #result_number {
                font-size: 34px;
                font-weight: bold;
            }
        """)

    def _init_db(self):
        self.db = DatabaseManager()
        self.db.init_db()
        self._refresh_history()

    def _bind_signals(self):
        self.btn_calculate.clicked.connect(self._on_calculate)
        self.btn_add_discount.clicked.connect(self._on_add_discount)
        self.btn_remove_discount.clicked.connect(self._on_remove_discount)
        self.btn_clear_discounts.clicked.connect(self._on_clear_discounts)
        self.btn_load_photo.clicked.connect(self._on_load_photo)
        self.btn_save_history.clicked.connect(self._on_save_history)
        self.btn_update_history.clicked.connect(self._on_update_history)
        self.btn_delete_history.clicked.connect(self._on_delete_history)
        self.btn_export_csv.clicked.connect(self._on_export_csv)

    def _on_calculate(self):
        price = self.spin_price.value()
        tax = self.spin_tax.value()

        if price <= 0:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть больше 0")
            return

        discounts = []
        for i in range(self.list_discounts.count()):
            text = self.list_discounts.item(i).text().replace("%", "").strip()
            try:
                discounts.append(float(text))
            except ValueError:
                pass

        if len(discounts) == 0 and self.spin_discount.value() > 0:
            discounts.append(self.spin_discount.value())

        current = price
        for d in discounts:
            current = current * (1 - d / 100)

        final_price = current * (1 + tax / 100)
        saved = price - current

        self.final_price = round(final_price, 2)
        self.saved = round(saved, 2)

        self.lbl_final_price.setText(f"{self.final_price:.2f} руб")
        self.lbl_saved.setText(f"Экономия: {self.saved:.2f} руб")

    def _on_add_discount(self):
        value = self.spin_discount.value()
        if value > 0:
            self.list_discounts.addItem(f"{value:.1f}%")
            self.spin_discount.setValue(0)

    def _on_remove_discount(self):
        row = self.list_discounts.currentRow()
        if row >= 0:
            self.list_discounts.takeItem(row)

    def _on_clear_discounts(self):
        self.list_discounts.clear()

    def _on_load_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if not path:
            return

        try:
            img = Image.open(path).convert("RGBA")
            img.thumbnail((320, 320), Image.LANCZOS)
            data = img.tobytes("raw", "RGBA")
            qimg = QImage(data, img.width, img.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg.copy())

            self.lbl_photo.setPixmap(pixmap)
            self.lbl_photo.setStyleSheet("border: none;")
            self.image_path = path
        except Exception as error:
            logging.error("photo error: %s", error)
            QMessageBox.critical(self, "Ошибка", str(error))

    def _on_save_history(self):
        if self.final_price is None:
            QMessageBox.warning(self, "Внимание", "Сначала выполните расчёт")
            return

        discounts = []
        for i in range(self.list_discounts.count()):
            discounts.append(self.list_discounts.item(i).text())
        discounts_text = ", ".join(discounts)
        if discounts_text == "":
            discounts_text = "0%"

        data = {
            "price": self.spin_price.value(),
            "discounts": discounts_text,
            "tax": self.spin_tax.value(),
            "final_price": self.final_price,
            "saved": self.saved,
            "image_path": self.image_path,
        }

        try:
            self.db.insert_record(data)
            self._refresh_history()
        except Exception as error:
            QMessageBox.critical(self, "Ошибка БД", str(error))

    def _on_update_history(self):
        if self.final_price is None:
            QMessageBox.warning(self, "Внимание", "Сначала выполните расчёт")
            return

        selected = self.table_history.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Внимание", "Выберите запись")
            return

        row = selected[0].row()
        record_id = self.table_history.item(row, 0).data(Qt.UserRole)

        discounts = []
        for i in range(self.list_discounts.count()):
            discounts.append(self.list_discounts.item(i).text())
        discounts_text = ", ".join(discounts)
        if discounts_text == "":
            discounts_text = "0%"

        data = {
            "price": self.spin_price.value(),
            "discounts": discounts_text,
            "tax": self.spin_tax.value(),
            "final_price": self.final_price,
            "saved": self.saved,
            "image_path": self.image_path,
        }

        try:
            self.db.update_record(record_id, data)
            self._refresh_history()
        except Exception as error:
            QMessageBox.critical(self, "Ошибка БД", str(error))

    def _on_delete_history(self):
        selected = self.table_history.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Внимание", "Выберите запись")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Удалить запись?")
        if reply != QMessageBox.Yes:
            return

        row = selected[0].row()
        record_id = self.table_history.item(row, 0).data(Qt.UserRole)

        try:
            self.db.delete_record(record_id)
            self._refresh_history()
        except Exception as error:
            QMessageBox.critical(self, "Ошибка БД", str(error))

    def _on_export_csv(self):
        records = self.db.get_all()
        if not records:
            QMessageBox.information(self, "Информация", "История пуста")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить CSV", "history.csv", "CSV Files (*.csv)"
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Цена", "Скидки", "Налог", "Итог", "Экономия", "Дата"]
                )
                for rec in records:
                    writer.writerow([
                        rec["price"],
                        rec["discounts"],
                        rec["tax"],
                        rec["final_price"],
                        rec["saved"],
                        rec["created_at"],
                    ])
        except Exception as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def _refresh_history(self):
        self.table_history.setRowCount(0)
        records = self.db.get_all()
        for i, rec in enumerate(records):
            self.table_history.insertRow(i)

            item = QTableWidgetItem(str(rec["price"]))
            item.setData(Qt.UserRole, rec["id"])
            self.table_history.setItem(i, 0, item)

            self.table_history.setItem(i, 1, QTableWidgetItem(str(rec["discounts"])))
            self.table_history.setItem(i, 2, QTableWidgetItem(str(rec["tax"])))
            self.table_history.setItem(i, 3, QTableWidgetItem(str(rec["final_price"])))
            self.table_history.setItem(i, 4, QTableWidgetItem(str(rec["saved"])))
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Выход",
            "Закрыть приложение?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.db is not None:
                self.db.close()
            event.accept()
        else:
            event.ignore()