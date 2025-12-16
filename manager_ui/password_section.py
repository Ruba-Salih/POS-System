# ملف: manager_ui/password_section.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3

class PasswordSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔐 تغيير كلمة المرور"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")

        self.old_pass_input = QLineEdit()
        self.old_pass_input.setPlaceholderText("كلمة المرور الحالية")
        self.old_pass_input.setEchoMode(QLineEdit.Password)

        self.new_pass_input = QLineEdit()
        self.new_pass_input.setPlaceholderText("كلمة المرور الجديدة")
        self.new_pass_input.setEchoMode(QLineEdit.Password)

        self.confirm_pass_input = QLineEdit()
        self.confirm_pass_input.setPlaceholderText("تأكيد كلمة المرور")
        self.confirm_pass_input.setEchoMode(QLineEdit.Password)

        save_btn = QPushButton("💾 حفظ التغيير")
        save_btn.clicked.connect(self.change_password)

        layout.addWidget(self.username_input)
        layout.addWidget(self.old_pass_input)
        layout.addWidget(self.new_pass_input)
        layout.addWidget(self.confirm_pass_input)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def change_password(self):
        username = self.username_input.text().strip()
        old_pass = self.old_pass_input.text().strip()
        new_pass = self.new_pass_input.text().strip()
        confirm_pass = self.confirm_pass_input.text().strip()

        if not username or not old_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "خطأ", "كلمة المرور الجديدة غير متطابقة")
            return

        conn = sqlite3.connect("pos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if not result:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم غير موجود")
        elif result[0] != old_pass:
            QMessageBox.warning(self, "خطأ", "كلمة المرور الحالية غير صحيحة")
        else:
            cursor.execute("UPDATE users SET password=? WHERE username=?", (new_pass, username))
            conn.commit()
            QMessageBox.information(self, "نجاح", "تم تغيير كلمة المرور")

        conn.close()
        self.username_input.clear()
        self.old_pass_input.clear()
        self.new_pass_input.clear()
        self.confirm_pass_input.clear()
