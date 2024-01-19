import sqlite3

db_name = 'my_db.db'
conn = sqlite3.connect(db_name, check_same_thread=False)
cursor = conn.cursor()


def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                order_date DATE NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY(product_id) REFERENCES products(product_id)
    )
    ''')

    cursor.execute('''
    INSERT INTO products (name, category, price)
    VALUES  ("laptop", "electronics", 15000),
            ("mouse", "electronics", 1000),
            ("golden toilet", "furniture", 1000000)
    ''')

    cursor.execute('''
    INSERT INTO customers (first_name, last_name, email)
    VALUES  ("edya", "bil", "qwerty@gmail.com"),
            ("Bill", "Gates", "nerd911@gmail.com"),
            ("Billy", "Doors", "pferd@gmail.com")
    ''')
    conn.commit()

#functions
def 