from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QStackedWidget, QComboBox,
    QDateEdit, QTableWidget, QTableWidgetItem, QFormLayout
)
from PyQt5.QtCore import Qt, QDate
import sqlite3
from datetime import date


class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("لوحة تحكم المدير")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(700)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Arial';
            }
            QPushButton {
                padding: 10px;
                font-size: 15px;
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1c5980;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # --- Navigation Buttons ---
        nav_layout = QHBoxLayout()
        buttons = [
            ("إدخال المصروفات", self.show_expenses_input),
            ("التقارير", self.show_reports),
            ("جدول المصروفات", self.show_expenses_table),
            ("جدول المبيعات", self.show_sales_table),
            ("إدارة العاملين", self.show_staff_management),
            ("تغيير كلمة المرور", self.show_password_change),
        ]
        for text, func in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            nav_layout.addWidget(btn)

        main_layout.addLayout(nav_layout)

        # --- Content Area ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Add all pages
        self.stack.addWidget(self.build_expenses_input())
        self.stack.addWidget(self.build_reports_page())
        self.stack.addWidget(self.build_expenses_table_page())
        self.stack.addWidget(self.build_sales_table_page())
        self.stack.addWidget(self.build_staff_page())
        self.stack.addWidget(self.build_password_change_page())

        self.setLayout(main_layout)

    # --- Navigation Functions ---
    def show_expenses_input(self): self.stack.setCurrentIndex(0)
    def show_reports(self): self.stack.setCurrentIndex(1)
    def show_expenses_table(self): self.stack.setCurrentIndex(2)
    def show_sales_table(self): self.stack.setCurrentIndex(3)
    def show_staff_management(self): self.stack.setCurrentIndex(4)
    def show_password_change(self): self.stack.setCurrentIndex(5)

    # --- Page 1: إدخال المصروفات ---
    def build_expenses_input(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("إدخال مصروف جديد"))

        self.exp_desc_input = QLineEdit()
        self.exp_desc_input.setPlaceholderText("الوصف")

        self.exp_amount_input = QLineEdit()
        self.exp_amount_input.setPlaceholderText("المبلغ")

        save_btn = QPushButton("حفظ المصروف")
        save_btn.clicked.connect(self.save_expense)

        layout.addWidget(self.exp_desc_input)
        layout.addWidget(self.exp_amount_input)
        layout.addWidget(save_btn)
        page.setLayout(layout)
        return page

    def save_expense(self):
        desc = self.exp_desc_input.text()
        try:
            amount = float(self.exp_amount_input.text())
            conn = sqlite3.connect("pos.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO expenses (description, amount) VALUES (?, ?)", (desc, amount))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "تم", "تم حفظ المصروف بنجاح ✅")
            self.exp_desc_input.clear()
            self.exp_amount_input.clear()
        except:
            QMessageBox.warning(self, "خطأ", "تأكد من إدخال مبلغ صحيح")

    # --- Page 2: التقارير ---
    def build_reports_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("التقرير:"))

        self.report_type = QComboBox()
        self.report_type.addItems(["تقرير يومي", "تقرير شهري"])

        self.report_date = QDateEdit(calendarPopup=True)
        self.report_date.setDate(QDate.currentDate())

        show_btn = QPushButton("عرض التقرير")
        show_btn.clicked.connect(self.show_report_logic)

        self.report_output = QLabel("")

        layout.addWidget(self.report_type)
        layout.addWidget(self.report_date)
        layout.addWidget(show_btn)
        layout.addWidget(self.report_output)
        page.setLayout(layout)
        return page

    def show_report_logic(self):
        conn = sqlite3.connect("pos.db")
        cur = conn.cursor()

        if self.report_type.currentText() == "تقرير يومي":
            selected_date = self.report_date.date().toString("yyyy-MM-dd")
            cur.execute("SELECT SUM(total) FROM sales WHERE DATE(created_at)=?", (selected_date,))
            sales = cur.fetchone()[0] or 0

            cur.execute("SELECT SUM(amount) FROM expenses WHERE DATE(created_at)=?", (selected_date,))
            expenses = cur.fetchone()[0] or 0

        else:
            selected_month = self.report_date.date().toString("yyyy-MM")
            cur.execute("SELECT SUM(total) FROM sales WHERE created_at LIKE ?", (f"{selected_month}%",))
            sales = cur.fetchone()[0] or 0

            cur.execute("SELECT SUM(amount) FROM expenses WHERE created_at LIKE ?", (f"{selected_month}%",))
            expenses = cur.fetchone()[0] or 0

        profit = sales - expenses
        self.report_output.setText(
            f"""
            🔹 المبيعات: {sales:.2f} ريال  
            🔹 المصروفات: {expenses:.2f} ريال  
            🔹 الربح: {profit:.2f} ريال
            """
        )
        conn.close()

    # --- Page 3: جدول المصروفات (مبدئي) ---
    def build_expenses_table_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("جدول المصروفات (تحت التطوير)"))
        page.setLayout(layout)
        return page

    # --- Page 4: جدول المبيعات (مبدئي) ---
    def build_sales_table_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("جدول المبيعات (تحت التطوير)"))
        page.setLayout(layout)
        return page

    # --- Page 5: إدارة العاملين (مبدئي) ---
    def build_staff_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("إدارة حسابات العاملين (تحت التطوير)"))
        page.setLayout(layout)
        return page

    # --- Page 6: تغيير كلمة المرور (مبدئي) ---
    def build_password_change_page(self):
        page = QWidget()
        layout = QFormLayout()
        layout.addRow(QLabel("تغيير كلمة المرور"))

        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.Password)
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)

        layout.addRow("كلمة المرور الحالية:", self.old_pass)
        layout.addRow("كلمة المرور الجديدة:", self.new_pass)
        save_btn = QPushButton("تحديث")
        layout.addWidget(save_btn)

        page.setLayout(layout)
        return page
