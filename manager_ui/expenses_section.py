# ملف: manager_ui/expenses_section.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3

class ExpensesSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.RightToLeft)
        layout = QVBoxLayout()

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("وصف المصروف")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("قيمة المصروف")

        save_btn = QPushButton("حفظ المصروف")
        save_btn.clicked.connect(self.save_expense)

        layout.addWidget(QLabel("إدخال مصروف جديد"))
        layout.addWidget(self.desc_input)
        layout.addWidget(self.amount_input)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_expense(self):
        desc = self.desc_input.text().strip()
        try:
            amount = float(self.amount_input.text())
            conn = sqlite3.connect("pos.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO expenses (description, amount) VALUES (?, ?)", (desc, amount))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "تم", "تم حفظ المصروف بنجاح ✅")
            self.desc_input.clear()
            self.amount_input.clear()
        except ValueError:
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال قيمة رقمية صحيحة")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ: {str(e)}")
