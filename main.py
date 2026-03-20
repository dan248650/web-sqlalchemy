from flask import redirect, render_template, request, make_response, jsonify
from pathlib import Path
import datetime

from routes.routes import register_all_blueprints
from configs.configs import app
from data.db import db
from data.__all_models import User, Jobs, Department, Role, Category
import uuid


def add_sample_users():
    db_sess = db.session

    if db_sess.query(User).filter(User.email != 'admin@mars.org').first() is not None:
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
        fs_uniquifier=str(uuid.uuid4()),
        modified_date=datetime.datetime.now()
    )
    captain.set_password('capitan_password')
    captain_role = db_sess.query(Role).filter_by(name='captain').first()
    captain.roles.append(captain_role)

    colonist1 = User(
        surname='Taylor',
        name='Robert',
        age=35,
        position='botanist',
        speciality='astrobotanist',
        address='module_2',
        email='robert.taylor@mars.org',
        fs_uniquifier=str(uuid.uuid4()),
        modified_date=datetime.datetime.now()
    )
    colonist1.set_password('taylor_password')

    colonist2 = User(
        surname='Jones',
        name='William',
        age=28,
        position='sys_operator',
        speciality='computer systems engineer',
        address='module_3',
        email='william.jones@mars.org',
        fs_uniquifier=str(uuid.uuid4()),
        modified_date=datetime.datetime.now()
    )
    colonist2.set_password('jones_password')

    colonist3 = User(
        surname='Harrington',
        name='Arthur',
        age=42,
        position='chemist',
        speciality='analytical chemist',
        address='module_1',
        email='arthur.harrington@mars.org',
        fs_uniquifier=str(uuid.uuid4()),
        modified_date=datetime.datetime.now()
    )
    colonist3.set_password('harrington_password')

    colonist4 = User(
        surname='Frost',
        name='Jack',
        age=32,
        position='pilot',
        speciality='spacecraft pilot',
        address='module_2',
        email='jack.frost@mars.org',
        fs_uniquifier=str(uuid.uuid4()),
        modified_date=datetime.datetime.now()
    )
    colonist4.set_password('frost_password')

    db_sess.add_all([captain, colonist1, colonist2, colonist3, colonist4])
    db_sess.commit()


def add_sample_jobs():
    db_sess = db.session

    if db_sess.query(Jobs).first() is not None:
        print("Работы уже существуют в базе данных")
        return

    scott = db_sess.query(User).filter(User.email == 'scott_chief@mars.org').first()
    taylor = db_sess.query(User).filter(User.email == 'robert.taylor@mars.org').first()
    jones = db_sess.query(User).filter(User.email == 'william.jones@mars.org').first()
    harrington = db_sess.query(User).filter(User.email == 'arthur.harrington@mars.org').first()
    frost = db_sess.query(User).filter(User.email == 'jack.frost@mars.org').first()
    if not all([scott, taylor, jones, harrington, frost]):
        print("Не все пользователи найдены в базе данных")
        return

    life_support = db_sess.query(Category).filter_by(name='life_support').first()
    research = db_sess.query(Category).filter_by(name='research').first()
    construction = db_sess.query(Category).filter_by(name='construction').first()
    terraforming = db_sess.query(Category).filter_by(name='terraforming').first()
    maintenance = db_sess.query(Category).filter_by(name='maintenance').first()
    emergency = db_sess.query(Category).filter_by(name='emergency').first()

    jobs = [
        Jobs(
            team_leader=scott.id,
            job='Deployment of residential modules 1 and 2',
            work_size=15,
            start_date=datetime.datetime.now() - datetime.timedelta(days=5),
            end_date=datetime.datetime.now() - datetime.timedelta(days=2),
            is_finished=True,
            categories=[construction, life_support]
        ),
        Jobs(
            team_leader=scott.id,
            job='Installation of life support systems',
            work_size=25,
            start_date=datetime.datetime.now() - datetime.timedelta(days=3),
            end_date=None,
            is_finished=False,
            categories=[life_support, construction]
        ),
        Jobs(
            team_leader=taylor.id,
            job='Soil analysis in sector A-7',
            work_size=10,
            start_date=datetime.datetime.now() - datetime.timedelta(days=1),
            end_date=datetime.datetime.now(),
            is_finished=True,
            categories=[research]
        ),
        Jobs(
            team_leader=jones.id,
            job='Maintenance of communication antennas',
            work_size=8,
            start_date=datetime.datetime.now(),
            end_date=None,
            is_finished=False,
            categories=[maintenance]
        ),
        Jobs(
            team_leader=harrington.id,
            job='Greenhouse experiment: Martian soil cultivation',
            work_size=30,
            start_date=datetime.datetime.now() - datetime.timedelta(days=10),
            end_date=datetime.datetime.now() - datetime.timedelta(days=1),
            is_finished=True,
            categories=[research, terraforming]
        ),
        Jobs(
            team_leader=frost.id,
            job='Drone reconnaissance of landing zone',
            work_size=12,
            start_date=datetime.datetime.now() - datetime.timedelta(days=2),
            end_date=None,
            is_finished=False,
            categories=[research]
        ),
        Jobs(
            team_leader=scott.id,
            job='Emergency drill: pressure drop simulation',
            work_size=5,
            start_date=datetime.datetime.now() - datetime.timedelta(hours=6),
            end_date=datetime.datetime.now() - datetime.timedelta(hours=1),
            is_finished=True,
            categories=[emergency]
        ),
    ]

    jobs[0].collaborators = [taylor, jones]
    jobs[1].collaborators = [harrington, frost]
    jobs[2].collaborators = [jones]
    jobs[3].collaborators = [taylor, frost]
    jobs[4].collaborators = [taylor]
    jobs[5].collaborators = [jones, harrington]
    jobs[6].collaborators = [taylor, jones, harrington, frost]

    db_sess.add_all(jobs)
    db_sess.commit()


def add_sample_departments():
    db_sess = db.session

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
def not_found(error):
    if request.path.startswith('/api/'):
        return make_response(jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404)
    return render_template('errors/error.html', error="Страница не найдена"), 404


@app.errorhandler(400)
def bad_request(error):
    if request.path.startswith('/api/'):
        return make_response(jsonify({
            'error': 'Bad Request',
            'message': str(error.description) if hasattr(error, 'description') else 'Invalid request'
        }), 400)
    return render_template('errors/error.html', error="Некорректный запрос"), 400


@app.errorhandler(403)
def forbidden(error):
    if request.path.startswith('/api/'):
        return make_response(jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403)
    return render_template('errors/error.html', error="Доступ запрещен"), 403


@app.errorhandler(401)
def unauthorized(error):
    if request.path.startswith('/api/'):
        return make_response(jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401)
    return render_template('errors/error.html', error="Требуется авторизация"), 401


@app.errorhandler(405)
def method_not_allowed(error):
    if request.path.startswith('/api/'):
        return make_response(jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for this endpoint'
        }), 405)
    return render_template('errors/error.html', error="Метод не разрешен"), 405


@app.errorhandler(500)
def internal_server_error(error):
    if request.path.startswith('/api/'):
        return make_response(jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal error occurred'
        }), 500)
    return render_template('errors/error.html', error="Внутренняя ошибка сервера"), 500


if __name__ == '__main__':
    with app.app_context():
        add_sample_users()
        add_sample_jobs()
        add_sample_departments()
    app.run(debug=True)
