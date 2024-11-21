from flask import Blueprint, render_template, request
import sqlite3

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@feedback_bp.route('/', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        conn = get_db_connection()
        conn.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
                     (name, email, message))
        conn.commit()
        conn.close()
    conn = get_db_connection()
    feedbacks = conn.execute('SELECT * FROM feedback').fetchall()
    conn.close()
    return render_template('feedback.html', feedbacks=feedbacks)
