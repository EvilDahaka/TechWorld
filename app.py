from flask import Flask, render_template
from models import init_db
from routes.feedback import feedback_bp
from routes.products import products_bp
from routes.admin import admin_bp
import sqlite3


app = Flask(__name__)
app.register_blueprint(admin_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(products_bp)
#app.register_blueprint(api_bp)

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect('db.sqlite')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            tag TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# @app.route('/products')
# def products():
#    return render_template('products.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)