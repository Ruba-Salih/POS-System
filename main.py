from PyQt5.QtWidgets import QApplication
import sys
from manager_ui.main_window import ManagerWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManagerWindow()
    window.show()
    sys.exit(app.exec_())
