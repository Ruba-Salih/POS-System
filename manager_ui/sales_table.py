# ملف: manager_ui/sales_table.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QDateEdit, QPushButton
from PyQt5.QtCore import QDate, Qt
import sqlite3

class SalesTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("📋 جدول المبيعات"))

        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel("اختر التاريخ:"))
        layout.addWidget(self.date_input)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["المنتج", "الكمية", "السعر", "الإجمالي", "التاريخ"])
        layout.addWidget(self.table)

        load_btn = QPushButton("تحميل المبيعات")
        load_btn.clicked.connect(self.load_data)
        layout.addWidget(load_btn)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        selected_date = self.date_input.date().toString("yyyy-MM-dd")
        conn = sqlite3.connect("pos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, quantity, price, total, created_at FROM sales WHERE DATE(created_at)=?", (selected_date,))
        data = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
