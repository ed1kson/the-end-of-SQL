import sqlite3
import datetime

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
def get_id_by_email(email):
    cursor.execute('''
        SELECT customer_id FROM customers WHERE email = (?)
        ''', (email,))
    return cursor.fetchall()

def sign_up(first_name, last_name, email, commit:bool):
    cursor.execute('''
        INSERT INTO customers(first_name, last_name, email)
        VALUES((?), (?), (?)) 
        ''', (first_name, last_name, email))
    if commit:
        conn.commit()

def apply_purchase(customer_id, product_id, quantity, commit:bool):
    date = datetime.datetime.now()

    cursor.execute('''
        INSERT INTO orders(customer_id, product_id, quantity, order_date)
        VALUES ((?), (?), (?), (?))
        ''', (customer_id, product_id, quantity, date))
    if commit:
        conn.commit()

def get_all_purchases_count():
    cursor.execute('''
        SELECT SUM(quantity) FROM orders
        ''')
    return cursor.fetchall()

def get_orders_per_customer():
    cursor.execute('''
        SELECT customers.customer_id, customers.first_name, customers.last_name, COUNT(orders.order_id) as order_count FROM customers
        INNER JOIN orders ON customers.customer_id = orders.customer_id
        GROUP BY customers.customer_id
        ''')
    return cursor.fetchall()

def get_products_list():
    cursor.execute('''
    SELECT * FROM products
    ''')
    return cursor.fetchall()

def get_avg_sum_per_order():
    cursor.execute('''
SELECT  
''')