from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("واجهة المدير")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        welcome = QLabel("مرحبًا بك في واجهة المدير")
        layout.addWidget(welcome)

        self.setLayout(layout)
