import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, image TEXT, tag TEXT)')

def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products

    