from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CashierWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("واجهة الكاشير")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(400)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f7;
            }
            QLabel {
                font-size: 16px;
            }
            QLineEdit {
                padding: 6px;
                font-size: 16px;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                background-color: #0078d7;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)

        layout = QVBoxLayout()

        # اسم المنتج
        row1 = QHBoxLayout()
        name_label = QLabel("اسم المنتج:")
        self.name_input = QLineEdit()
        row1.addWidget(name_label)
        row1.addWidget(self.name_input)

        # السعر
        row2 = QHBoxLayout()
        price_label = QLabel("السعر:")
        self.price_input = QLineEdit()
        row2.addWidget(price_label)
        row2.addWidget(self.price_input)

        # الكمية
        row3 = QHBoxLayout()
        qty_label = QLabel("الكمية:")
        self.qty_input = QLineEdit()
        row3.addWidget(qty_label)
        row3.addWidget(self.qty_input)

        # زر الحفظ
        self.button = QPushButton("تسجيل البيع")
        self.button.clicked.connect(self.register_sale)

        # إضافة العناصر إلى الواجهة
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def register_sale(self):
        try:
            name = self.name_input.text()
            price = float(self.price_input.text())
            qty = int(self.qty_input.text())
            total = price * qty
            QMessageBox.information(self, "تم", f"تم تسجيل البيع بنجاح\nالإجمالي: {total:.2f} ريال")
        except:
            QMessageBox.warning(self, "خطأ", "تأكد من إدخال السعر والكمية بشكل صحيح")
