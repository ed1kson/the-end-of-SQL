import sqlite3
import datetime
import math

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

def get_products_list():
    cursor.execute('''
    SELECT * FROM products
    ''')
    return cursor.fetchall()

def get_all_income():
    cursor.execute('''
    SELECT SUM(quantity), price FROM ORDERS
    INNER JOIN products ON orders.product_id = products.product_id
    GROUP BY products.product_id
    ''')
    income = sum([math.prod(row) for row in cursor.fetchall()])
    return income

def get_order_count_per_customer():
    cursor.execute('''
    SELECT first_name, email, count(orders.order_id) FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.customer_id''')
    return cursor.fetchall()

def get_avg_check():
    cursor.execute('''
    SELECT orders.order_id, orders.quantity, products.price FROM orders
    INNER JOIN products ON orders.product_id = products.product_id
    ''')

    check = [(row[1]*row[2]) for row in cursor.fetchall()]
    check = sum(check)/len(check)

    return check
