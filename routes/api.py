from flask import Blueprint, jsonify, request, session
from models import (
    get_db_connection, get_products, get_orders, get_order_details,
    add_order, update_order_status, delete_order, get_current_user, add_feedback
)
import bcrypt
import re

api_bp = Blueprint('api', __name__)

# Products endpoints
@api_bp.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        conn = get_db_connection()
        products = conn.execute("SELECT * FROM products").fetchall()
        conn.close()
        return jsonify([dict(product) for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Orders endpoints
@api_bp.route('/api/orders', methods=['GET'])
def get_all_orders():
    try:
        conn = get_db_connection()
        orders = conn.execute("SELECT * FROM orders").fetchall()
        conn.close()
        return jsonify([dict(order) for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        conn = get_db_connection()
        order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        items = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
        conn.close()
        return jsonify({
            'order': dict(order),
            'items': [dict(item) for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'address' not in data or 'cart' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Перевірка формату email
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        add_order(data['email'], data['address'], data['cart'])
        return jsonify({'message': 'Order created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400

        update_order_status(order_id, data['status'])
        return jsonify({'message': 'Order updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    try:
        delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User endpoints (Registration, Login, Logout)
@api_bp.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['username', 'email', 'password', 'confirm_password']):
            return jsonify({'error': 'Missing required fields'}), 400

        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        if len(username) < 3 or len(password) < 8:
            return jsonify({'error': 'Username or password is too short'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            conn.close()
            return jsonify({'error': 'Email is already in use'}), 400

        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                     (username, email, hashed_password))
        conn.commit()
        conn.close()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        email = data['email']
        password = data['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']
            conn.close()
            return jsonify({'message': 'Login successful'}), 200
        conn.close()
        return jsonify({'error': 'Invalid email or password'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/logout', methods=['POST'])
def logout_user():
    try:
        session.pop('user_id', None)  # Видаляємо user_id з сесії
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Feedback endpoints
@api_bp.route('/api/feedback', methods=['POST'])
def create_feedback():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({'error': 'Missing required fields'}), 400

        add_feedback(data['name'], data['email'], data['message'])
        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cart endpoints (Add to cart, Remove from cart, Clear cart)
@api_bp.route('/api/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        if not data or 'product_id' not in data or 'quantity' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        conn = get_db_connection()
        conn.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', 
                     (user_id, data['product_id'], data['quantity']))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Product added to cart'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/cart', methods=['DELETE'])
def clear_cart():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        conn = get_db_connection()
        conn.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Cart cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
