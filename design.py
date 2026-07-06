from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
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
        self.centralWidget().setLayout(main_layout)

        self.lbl_title = QLabel("Калькулятор скидок")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_title)