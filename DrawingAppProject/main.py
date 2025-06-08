from PySide6.QtWidgets import QApplication
from app.window import MyWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyWindow()
    main_window.show()
    app.exec()