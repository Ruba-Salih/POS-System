# ملف: manager_ui/reports_section.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QDateEdit
from PyQt5.QtCore import QDate, Qt
import sqlite3

class ReportsSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📊 عرض التقارير"))

        self.report_type = QComboBox()
        self.report_type.addItems(["تقرير يومي", "تقرير شهري"])

        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())

        self.output_label = QLabel("")

        generate_btn = QPushButton("عرض التقرير")
        generate_btn.clicked.connect(self.generate_report)

        layout.addWidget(QLabel("نوع التقرير:"))
        layout.addWidget(self.report_type)
        layout.addWidget(QLabel("اختر التاريخ:"))
        layout.addWidget(self.date_input)
        layout.addWidget(generate_btn)
        layout.addWidget(self.output_label)

        self.setLayout(layout)

    def generate_report(self):
        selected_type = self.report_type.currentText()
        selected_date = self.date_input.date()

        conn = sqlite3.connect("pos.db")
        cursor = conn.cursor()

        if selected_type == "تقرير يومي":
            date_str = selected_date.toString("yyyy-MM-dd")
            cursor.execute("SELECT SUM(total) FROM sales WHERE DATE(created_at)=?", (date_str,))
            sales = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(amount) FROM expenses WHERE DATE(created_at)=?", (date_str,))
            expenses = cursor.fetchone()[0] or 0

        elif selected_type == "تقرير شهري":
            month_str = selected_date.toString("yyyy-MM")
            cursor.execute("SELECT SUM(total) FROM sales WHERE created_at LIKE ?", (f"{month_str}%",))
            sales = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(amount) FROM expenses WHERE created_at LIKE ?", (f"{month_str}%",))
            expenses = cursor.fetchone()[0] or 0

        conn.close()

        profit = sales - expenses

        self.output_label.setText(
            f"""
📅 التاريخ: {selected_date.toString("yyyy-MM-dd")}
💰 المبيعات: {sales:.2f} ريال
📉 المصروفات: {expenses:.2f} ريال
🟢 الربح: {profit:.2f} ريال
            """
        )
