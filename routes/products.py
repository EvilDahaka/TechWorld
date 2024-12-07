from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from models import get_db_connection, add_order
from .user import auth

products_bp = Blueprint('products', __name__)

get_db_connection()

@products_bp.before_request
def check_auth():
    if not auth():  # Викликається перед кожним запитом до цього блоку
        return redirect(url_for('user.login'))

# Сторінка продуктів із фільтром за тегом
@products_bp.route('/products')
def products():

    tag = request.args.get('tag')
    products = get_products(tag=tag)
    return render_template('products.html', products=products)

# Додавання товару до кошика
@products_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = session.get('user_id')  # ID користувача з сесії
    conn = get_db_connection()

    # Отримуємо дані продукту з бази даних
    product_query = "SELECT name, price FROM products WHERE id = ?"
    product = conn.execute(product_query, (product_id,)).fetchone()

    if not product:
        # Якщо продукт не знайдено, повертаємо помилку
        conn.close()
        return "Продукт не знайдено", 404

    # Перевіряємо, чи продукт вже в кошику користувача
    query = "SELECT quantity FROM cart WHERE user_id = ? AND name = ?"
    existing_product = conn.execute(query, (user_id, product['name'])).fetchone()

    if existing_product:
        # Якщо продукт вже в кошику, збільшуємо кількість
        new_quantity = existing_product['quantity'] + 1
        update_query = "UPDATE cart SET quantity = ? WHERE user_id = ? AND name = ?"
        conn.execute(update_query, (new_quantity, user_id, product['name']))
    else:
        # Якщо продукт ще не в кошику, додаємо його
        insert_query = """
            INSERT INTO cart (user_id, name, price, quantity)
            VALUES (?, ?, ?, ?)
        """
        conn.execute(insert_query, (user_id, product['name'], product['price'], 1))

    conn.commit()
    conn.close()
    return redirect(url_for('products.products'))


@products_bp.route('/cart')
def cart():
    cart = get_cart()
    total = 0
    for item in cart:
        # Перевірка, чи є ці дані в Row
        if 'price' in item.keys() and 'quantity' in item.keys():
            try:
                # Перетворення значень на числові
                price = float(item['price'])  # Приведення ціни до числа
                quantity = int(item['quantity'])  # Приведення кількості до цілого
                total += price * quantity
            except ValueError as e:
                print(f"Помилка конвертації: {e}, товар: {item}")
        else:
            print(f"Недостає ключів у товарі: {item}")
    return render_template('cart.html', cart=cart, total=total)




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
# Запис замовлення 
@products_bp.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    email = request.form['email']
    address = request.form['address']
    add_order(email, address, cart)
    session['cart'] = {}
    return redirect(url_for('products.products'))

def get_cart():
    conn = get_db_connection()
    user_id = session.get('user_id')
    products = conn.execute("SELECT * FROM cart WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return products
@products_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    conn = get_db_connection()
    user_id = auth()  # Перевірка автентифікації та отримання user_id

    if not user_id:  # Якщо user_id не знайдено
        return "Unauthorized", 401

    # Видаляємо записи з таблиці cart для user_id
    conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    # Перенаправлення на сторінку кошика
    return redirect(url_for('products.cart'))

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
    