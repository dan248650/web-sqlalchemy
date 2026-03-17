from flask import redirect, render_template
from pathlib import Path
import datetime

from routes.routes import register_all_blueprints
from configs.configs import app
from data.db_session import create_session
from data.__all_models import User


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
        email='mark.watney@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist1.hashed_password = 'watney_password'

    colonist2 = User(
        surname='Jones',
        name='William',
        age=28,
        position='sys_operator',
        speciality='computer systems engineer',
        address='module_3',
        email='beth.johanssen@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist2.hashed_password = 'johanssen_password'

    colonist3 = User(
        surname='Harrington',
        name='Arthur',
        age=42,
        position='chemist',
        speciality='analytical chemist',
        address='module_1',
        email='alex.vogel@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist3.hashed_password = 'vogel_password'

    colonist4 = User(
        surname='Frost',
        name='Jack',
        age=32,
        position='pilot',
        speciality='spacecraft pilot',
        address='module_2',
        email='rick.martinez@mars.org',
        modified_date=datetime.datetime.now()
    )
    colonist4.hashed_password = 'martinez_password'

    db_sess.add(captain)
    db_sess.add(colonist1)
    db_sess.add(colonist2)
    db_sess.add(colonist3)
    db_sess.add(colonist4)
    db_sess.commit()


register_all_blueprints(app)


@app.route('/', methods=['GET', 'POST'])
def init():
    return render_template('layouts/base.html')


if __name__ == '__main__':
    with app.app_context():
        add_sample_users()
    app.run(debug=True)
