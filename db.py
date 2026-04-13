import sqlite3

conn = sqlite3.connect('dairy.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            product TEXT,
            quantity INTEGER,
            revenue REAL
        )
    ''')
    conn.commit()

def insert_data(date, product, quantity, revenue):
    c.execute('INSERT INTO sales(date, product, quantity, revenue) VALUES (?, ?, ?, ?)',
              (date, product, quantity, revenue))
    conn.commit()

def get_data():
    c.execute('SELECT * FROM sales')
    return c.fetchall()
