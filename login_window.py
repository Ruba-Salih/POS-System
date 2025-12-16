from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3
import cashier_window
import manager_window

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل الدخول")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        self.label_user = QLabel("اسم المستخدم:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("كلمة المرور:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.button = QPushButton("دخول")
        self.button.clicked.connect(self.login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def login(self):
        user = self.input_user.text()
        pw = self.input_pass.text()

        conn = sqlite3.connect("pos.db")
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (user, pw))
        result = cur.fetchone()
        conn.close()

        if result:
            role = result[0]
            self.hide()
            if role == "cashier":
                self.cashier = cashier_window.CashierWindow()
                self.cashier.show()
            else:
                self.manager = manager_window.ManagerWindow()
                self.manager.show()
        else:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")
