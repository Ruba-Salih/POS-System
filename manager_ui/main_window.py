# ملف: manager_ui/main_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtCore import Qt

from manager_ui.expenses_section import ExpensesSection
from manager_ui.reports_section import ReportsSection
from manager_ui.expenses_table import ExpensesTable
from manager_ui.sales_table import SalesTable
from manager_ui.staff_section import StaffSection
from manager_ui.password_section import PasswordSection

class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام إدارة الكافتيريا - المدير")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(600)

        layout = QVBoxLayout()

        # عناصر التنقل العلوية
        self.buttons_layout = QVBoxLayout()
        self.stack = QStackedWidget()

        self.expenses_section = ExpensesSection()
        self.reports_section = ReportsSection()
        self.expenses_table = ExpensesTable()
        self.sales_table = SalesTable()
        self.staff_section = StaffSection()
        self.password_section = PasswordSection()

        self.stack.addWidget(self.expenses_section)
        self.stack.addWidget(self.reports_section)
        self.stack.addWidget(self.expenses_table)
        self.stack.addWidget(self.sales_table)
        self.stack.addWidget(self.staff_section)
        self.stack.addWidget(self.password_section)

        # أزرار التنقل
        self.add_nav_button("📥 إدخال المصروفات", 0)
        self.add_nav_button("📊 التقارير", 1)
        self.add_nav_button("📋 جدول المصروفات", 2)
        self.add_nav_button("💵 جدول المبيعات", 3)
        self.add_nav_button("👥 إدارة العاملين", 4)
        self.add_nav_button("🔐 تغيير كلمة المرور", 5)

        layout.addLayout(self.buttons_layout)
        layout.addWidget(self.stack)

        self.setLayout(layout)

    def add_nav_button(self, label, index):
        btn = QPushButton(label)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(index))
        self.buttons_layout.addWidget(btn)
