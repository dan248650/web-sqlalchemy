from flask import Flask, redirect, flash
from flask_security import Security, SQLAlchemyUserDatastore, current_user
import os
import uuid
from functools import wraps
from locale import setlocale, Error, LC_ALL


from data.db import db
from data.__all_models import User, Role, Category
from utils.generation_password import generate_password_for_user


def setup_locale():
    locales = ['ru_RU.utf8', 'rus_rus', 'ru_RU', 'russian']
    for locale in locales:
        try:
            setlocale(LC_ALL, locale)
            print(f"Locale set to {locale}")
            return
        except Error:
            continue
    print("Warning: Russian locale not available, using default")


setup_locale()

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')
DB_DIR = os.path.join(BASE_DIR, '..', 'db')
DB_PATH = os.path.join(DB_DIR, 'database.db')

app.template_folder = TEMPLATE_DIR
app.static_folder = STATIC_DIR

os.makedirs(DB_DIR, exist_ok=True)

app.config.update(
    SECRET_KEY='super-secret-key',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_PATH}',
    SECURITY_PASSWORD_SALT='salt-for-password-hashing',
    SECURITY_LOGIN_URL='/login',
    SECURITY_LOGOUT_URL='/logout',
    SECURITY_REGISTER_URL='/register',
    SECURITY_REGISTERABLE=True,
    SECURITY_SEND_REGISTER_EMAIL=False,
    SECURITY_LOGIN_USER_TEMPLATE='auth/login.html',
    SECURITY_REGISTER_USER_TEMPLATE='auth/register.html',
    YANDEX_MAPS_API_KEY='8013b162-6b42-4997-9691-77b7074026e0'
)

db.init_app(app)

with app.app_context():
    db.create_all()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_blueprint=False)


def init_database():
    with app.app_context():
        try:
            roles = ['admin', 'captain', 'user']
            for role_name in roles:
                role = db.session.query(Role).filter_by(name=role_name).first()
                if not role:
                    role = Role(name=role_name)
                    db.session.add(role)

            db.session.commit()

            categories = [
                {'name': 'life_support', 'description': 'Обеспечение жизнедеятельности'},
                {'name': 'research', 'description': 'Научные исследования'},
                {'name': 'construction', 'description': 'Строительство и монтаж'},
                {'name': 'terraforming', 'description': 'Терраформирование'},
                {'name': 'maintenance', 'description': 'Техническое обслуживание'},
                {'name': 'emergency', 'description': 'Аварийные работы'}
            ]

            for cat_data in categories:
                category = db.session.query(Category).filter_by(name=cat_data['name']).first()
                if not category:
                    category = Category(
                        name=cat_data['name'],
                        description=cat_data['description']
                    )
                    db.session.add(category)

            db.session.commit()

            admin_role = db.session.query(Role).filter_by(name='admin').first()
            admin = db.session.query(User).filter_by(email='admin@mars.org').first()

            if not admin and admin_role:
                password = generate_password_for_user()
                print(f"Admin password: {password}")

                admin_user = User(
                    name='Admin',
                    surname='',
                    email='admin@mars.org',
                    city_from='Moscow, Russia',
                    fs_uniquifier=str(uuid.uuid4()),
                    active=True
                )
                admin_user.set_password(password)
                admin_user.roles.append(admin_role)

                db.session.add(admin_user)
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при инициализации БД: {e}")


init_database()


@app.context_processor
def inject_user():
    return dict(current_user=current_user)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Необходимо войти в систему', 'warning')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
