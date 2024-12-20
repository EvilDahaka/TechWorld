import sqlite3
from flask import session
from datetime import datetime
def init_db():
    conn = sqlite3.connect('data/db.sqlite')

    # Таблиця feedback
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    # Таблиця products
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            specifications TEXT,
            image TEXT,
            tag TEXT
        )
    ''')

    # Таблиця cart
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
);
    ''')

    # Таблиця orders
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Таблиця order_items
    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


def get_products():
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products").fetchone()
    conn.close()
    return product

def get_db_connection():
    conn = sqlite3.connect('data/db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def add_order(email, address, cart):
    conn = get_db_connection()
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (email, address, total_price, status, date) VALUES (?, ?, ?, ?, ?)',
                (email, address, total_price, 'New', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    order_id = cur.lastrowid
    for item in cart:
        cur.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                    (order_id, item['product_id'], item['quantity']))
    conn.commit()
    conn.close()


def get_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return orders

def get_order_details(order_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    items = conn.execute('SELECT oi.quantity, p.name, p.price FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = ?', (order_id,)).fetchall()
    conn.close()
    return order, items

def update_order_status(order_id, status):
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()

def get_current_user():
    """
    Функція для отримання поточного користувача з сесії.
    Повертає дані користувача або None, якщо користувач не авторизований.
    """
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            user = cur.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return user
        finally:
            conn.close()
    return None

def add_feedback(name, email, message):
    """
    Функція для додавання нового відгуку в базу даних.
    Параметри:
    - name: ім'я користувача
    - email: email користувача
    - message: текст відгуку
    """
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
            (name, email, message)
        )
        conn.commit()
    finally:
        conn.close()

def get_products(id=None, tag=None, name=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if id is not None: 
        query += " AND id = ?"
        params.append(id)
    if tag is not None:
        query += " AND tag = ?"
        params.append(tag)
    if name is not None:
        query += " AND name = ?"
        params.append(name)

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()

    return results
    
