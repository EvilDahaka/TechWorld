import re
import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import get_db_connection

user_bp = Blueprint('user', __name__)

def validate_registration_data(username, email, password, confirm_password):
    if not username or not email or not password or not confirm_password:
        return "Всі поля є обов'язковими."
    if len(username) < 3:
        return "Ім'я користувача повинно бути не менше 3 символів."
    if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        return "Ім'я користувача може містити тільки букви, цифри, _, . або -."
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return "Некоректний формат email."
    if len(password) < 8:
        return "Пароль повинен бути не менше 8 символів."
    if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        return "Пароль повинен містити букви та цифри."
    if password != confirm_password:
        return "Паролі не співпадають."
    return None

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
            conn.close()  # Закрити з'єднання після завершення
    return None


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        validation_error = validate_registration_data(username, email, password, confirm_password)
        print(validation_error)
        if validation_error:
            return redirect(url_for('user.register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()  # Отримати нове з'єднання
        try:
            existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
            if existing_user:
                print("Користувач із таким ім'ям або email вже існує.") #перевірка на існуючий ім'я чи email
                return redirect(url_for('user.register'))

            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                         (username, email, hashed_password))
            conn.commit()
            print('записанна в базу даних')
        finally:
            conn.close()  # Закрити з'єднання

        print("Реєстрація успішна! Ви можете увійти в систему.")
        return redirect(url_for('user.login'))

    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if user:
                stored_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Успішний вхід
                    session['user_id'] = user['id']
                    flash("Ви успішно увійшли.")
                    return redirect(url_for('home'))
            flash("Невірний email або пароль.")
        finally:
            conn.close()  # Закриваємо з'єднання
    return render_template('login.html')


@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Видаляємо user_id з сесії
    print("Ви вийшли з системи.")
    return redirect(url_for('home'))
#видає none якщо не найде юзера а так видає його id 
def auth():
    return session.get('user_id') is not None
