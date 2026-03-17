from flask import redirect, render_template
from pathlib import Path
import datetime

from routes.routes import register_all_blueprints
from configs.configs import app
from data.db_session import create_session
from data.__all_models import User, Jobs, Department


def add_sample_users():
    db_sess = create_session()

    if db_sess.query(User).first() is not None:
        print("Пользователи уже существуют в базе данных")
        return

    captain = User(
        surname='Scott',
        name='Ridley',
        age=21,
        position='captain',
        speciality='research engineer',
        address='module_1',
        email='scott_chief@mars.org',
        modified_date=datetime.datetime.now()
    )
    captain.hashed_password = 'capitan_password'  # Пока без хэшей

    colonist1 = User(
        surname='Taylor',
        name='Robert',
        age=35,
        position='botanist',
        speciality='astrobotanist',
        address='module_2',
        email='robert.taylor@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist1.hashed_password = 'taylor_password'

    colonist2 = User(
        surname='Jones',
        name='William',
        age=28,
        position='sys_operator',
        speciality='computer systems engineer',
        address='module_3',
        email='william.jones@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist2.hashed_password = 'jones_password'

    colonist3 = User(
        surname='Harrington',
        name='Arthur',
        age=42,
        position='chemist',
        speciality='analytical chemist',
        address='module_1',
        email='arthur.harrington@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist3.hashed_password = 'harrington_password'

    colonist4 = User(
        surname='Frost',
        name='Jack',
        age=32,
        position='pilot',
        speciality='spacecraft pilot',
        address='module_2',
        email='jack.frost@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist4.hashed_password = 'frost_password'

    db_sess.add(captain)
    db_sess.add(colonist1)
    db_sess.add(colonist2)
    db_sess.add(colonist3)
    db_sess.add(colonist4)
    db_sess.commit()


def add_first_job():
    db_sess = create_session()

    if db_sess.query(Jobs).first() is not None:
        print("Работы уже существуют в базе данных")
        return

    scott = db_sess.query(User).filter(User.email == 'scott_chief@mars.org').first()

    if not scott:
        print("Капитан не найден в базе данных")
        return

    first_job = Jobs(
        team_leader=scott.id,
        job='deployment of residential modules 1 and 2',
        work_size=15,
        collaborators="2, 3",
        start_date=datetime.date.today(),
        end_date=None,
        is_finished=False
    )

    db_sess.add(first_job)
    db_sess.commit()


def add_sample_departments():
    db_sess = create_session()

    if db_sess.query(Department).first() is not None:
        print("Департаменты уже существуют в базе данных")
        return

    scott = db_sess.query(User).filter(User.email == 'scott_chief@mars.org').first()
    taylor = db_sess.query(User).filter(User.email == 'robert.taylor@mars.org').first()
    jones = db_sess.query(User).filter(User.email == 'william.jones@mars.org').first()
    harrington = db_sess.query(User).filter(User.email == 'arthur.harrington@mars.org').first()
    frost = db_sess.query(User).filter(User.email == 'jack.frost@mars.org').first()

    if not all([scott, taylor, jones, harrington, frost]):
        print("Не все пользователи найдены в базе данных")
        return

    engineering_dept = Department(
        title='Engineering Department',
        chief=scott.id,
        email='engineering@mars.org'
    )
    engineering_dept.members = [taylor, jones, frost]

    science_dept = Department(
        title='Science Department',
        chief=harrington.id,
        email='science@mars.org'
    )
    science_dept.members = [taylor, harrington]

    security_dept = Department(
        title='Security Department',
        chief=frost.id,
        email='security@mars.org'
    )
    security_dept.members = [frost, scott]

    db_sess.add_all([engineering_dept, science_dept, security_dept])
    db_sess.commit()


register_all_blueprints(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/error.html', error="Страница не найдена"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/error.html', error="Внутренняя ошибка сервера"), 500


if __name__ == '__main__':
    with app.app_context():
        add_sample_users()
        add_first_job()
        add_sample_departments()
    app.run(debug=True)
