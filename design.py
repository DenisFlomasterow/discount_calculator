from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QDoubleSpinBox, QFrame
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор скидок")
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)

        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        self.centralWidget().setLayout(main_layout)

        self.lbl_title = QLabel("Калькулятор скидок")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_title)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout, 1)

        photo_card = QFrame()
        photo_layout = QVBoxLayout(photo_card)
        self.lbl_photo = QLabel("Фото товара")
        self.lbl_photo.setAlignment(Qt.AlignCenter)
        self.lbl_photo.setStyleSheet("border: 2px dashed #aaaaaa;")
        photo_layout.addWidget(self.lbl_photo, 1)
        self.btn_load_photo = QPushButton("Загрузить фото")
        photo_layout.addWidget(self.btn_load_photo)
        content_layout.addWidget(photo_card, 1)

        right_layout = QVBoxLayout()
        content_layout.addLayout(right_layout, 1)

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
        right_layout.addLayout(form_layout)

        self.btn_calculate = QPushButton("Рассчитать")
        right_layout.addWidget(self.btn_calculate)
        right_layout.addStretch()