from flask import Blueprint, render_template, request
from models import get_db_connection

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

get_db_connection()

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

def get_feedback():
    conn = get_db_connection()
    feedback = conn.execute('SELECT * FROM feedback').fetchall()
    conn.close()
    return feedback
