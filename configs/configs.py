from flask import Flask
import os
from locale import setlocale, Error, LC_ALL

from data.db_session import global_init

try:
    setlocale(LC_ALL, 'ru_RU.utf8')
except Error:
    try:
        setlocale(LC_ALL, 'rus_rus')
    except Error:
        print("Выбранная локализация недоступна. Используется локализация по умолчанию.")


app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
app.template_folder = TEMPLATE_DIR

app.static_folder = os.path.join(BASE_DIR, '..', 'static')

DB_DIR = os.path.join(BASE_DIR, '..', 'db')
DB_PATH = os.path.join(DB_DIR, 'database.db')


if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR, exist_ok=True)


app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECURITY_PASSWORD_SALT'] = 'salt-for-password-hashing'

global_init(DB_PATH)


@app.before_request
def start_db():
    with app.app_context():
        pass
