import sqlite3

conn = sqlite3.connect("pos.db")
c = conn.cursor()

# جدول المصروفات
c.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    amount REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# جدول المبيعات
c.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    quantity INTEGER,
    price REAL,
    total REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# جدول المستخدمين
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('manager', 'cashier')) DEFAULT 'cashier'
)
''')

# إدخال حساب المدير مبدئيًا
try:
    c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'manager')")
except:
    pass

conn.commit()
conn.close()
print("✔️ قاعدة البيانات جاهزة")
