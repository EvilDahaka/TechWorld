from flask import Flask, render_template, session
from models import init_db
from routes.feedback import feedback_bp
from routes.products import products_bp
from routes.admin import admin_bp
from routes.api import api_bp
from routes.user import user_bp, auth


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(admin_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(products_bp)
app.register_blueprint(api_bp)
app.register_blueprint(user_bp)




# Ініціалізація бази даних

init_db()
#перевірка аутентифікація користувача?
@app.context_processor
def inject_auth():
    return {'auth': auth()}

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)