import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from database import init_db

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
