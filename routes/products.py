from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
import sqlite3

# Ініціалізація Blueprint
products_bp = Blueprint('products', __name__)

# Функція підключення до бази даних
def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# Функція отримання продукту за ID
def get_product_by_id(product_id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return product

# Сторінка продуктів із фільтром за тегом
@products_bp.route('/products')
def products():
    tag = request.args.get('tag')
    conn = get_db_connection()
    if tag:
        query = "SELECT * FROM products WHERE tag = ?"
        products = conn.execute(query, (tag,)).fetchall()
    else:
        query = "SELECT * FROM products"
        products = conn.execute(query).fetchall()
    conn.close()
    return render_template('products.html', products=products)

# Додавання товару до кошика
@products_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Продукт не знайдено"}), 404

    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': 1
        }

    session['cart'] = cart
    session.modified = True
    return jsonify({"message": "Товар додано до кошика", "cart": cart})

# Перегляд кошика
@products_bp.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', {})
    return jsonify({"cart": cart})

# Видалення товару з кошика
@products_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        session.modified = True
        return jsonify({"message": "Товар видалено з кошика", "cart": cart})
    return jsonify({"error": "Товар не знайдено в кошику"}), 404

# Очищення кошика
@products_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return jsonify({"message": "Кошик очищено"})
