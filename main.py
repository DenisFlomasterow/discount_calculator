import logging
import sys

from PyQt5.QtWidgets import QApplication
from design import MainWindow

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    app = QApplication(sys.argv)
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as error:
        logging.error("start error: %s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
