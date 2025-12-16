# ملف: manager_ui/staff_section.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import sqlite3

class StaffSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("👥 إدارة العاملين"))

        # نموذج إضافة مستخدم
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.role_select = QComboBox()
        self.role_select.addItems(["cashier", "manager"])

        add_btn = QPushButton("➕ إضافة مستخدم")
        add_btn.clicked.connect(self.add_user)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("الدور:"))
        layout.addWidget(self.role_select)
        layout.addWidget(add_btn)

        # جدول المستخدمين
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["المعرف", "اسم المستخدم", "الدور", "حذف"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        conn = sqlite3.connect("pos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user[0])))
            self.table.setItem(row, 1, QTableWidgetItem(user[1]))
            self.table.setItem(row, 2, QTableWidgetItem(user[2]))

            delete_btn = QPushButton("🗑 حذف")
            delete_btn.clicked.connect(lambda _, user_id=user[0]: self.delete_user(user_id))
            self.table.setCellWidget(row, 3, delete_btn)

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_select.currentText()

        if not username or not password:
            QMessageBox.warning(self, "خطأ", "يرجى ملء كل الحقول")
            return

        try:
            conn = sqlite3.connect("pos.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "نجاح", "تمت إضافة المستخدم")
            self.username_input.clear()
            self.password_input.clear()
            self.load_users()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم موجود بالفعل")

    def delete_user(self, user_id):
        confirm = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا المستخدم؟")
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect("pos.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            self.load_users()
