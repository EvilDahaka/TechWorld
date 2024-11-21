from flask import Blueprint, render_template
import sqlite3

products_bp = Blueprint('products', __name__, url_prefix='/products')

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@products_bp.route('/')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)
