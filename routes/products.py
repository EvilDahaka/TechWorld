from flask import Blueprint, render_template, request
import sqlite3

products_bp = Blueprint('products', __name__)

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@products_bp.route('/product', methods=['GET'])
def products():
    # Отримуємо параметр "tag" із запиту
    tag = request.args.get('tag')
    
    conn = get_db_connection()
    
    if tag:
        # Якщо тег вказаний, фільтруємо продукти за тегом
        query = "SELECT * FROM products WHERE tag = ?"
        products = conn.execute(query, (tag,)).fetchall()
    else:
        # Якщо тег не вказаний, отримуємо всі продукти
        query = "SELECT * FROM products"
        products = conn.execute(query).fetchall()
    
    conn.close()
    
    return render_template('products.html', products=products)


@products_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    products = get_products() # type: ignore # type: ignore
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', {}) # type: ignore
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': 1}
        session['cart'] = cart # type: ignore
    return redirect(url_for('shop.shop')) # type: ignore
