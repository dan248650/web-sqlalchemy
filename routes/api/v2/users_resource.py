from flask_restful import Resource, abort
from flask_security import current_user
from data.db import db
from data.__all_models import User, Role
from configs.configs import login_required
from routes.api.v2.parsers.user_parser import user_parser, user_update_parser
import uuid


class UsersListResource(Resource):
    method_decorators = [login_required]

    def get(self):
        if not current_user.is_admin():
            abort(403, error='Permission denied', message='Требуются права администратора')

        users = db.session.query(User).all()
        return {
            'users': [user.to_dict(only=('id', 'surname', 'name', 'email', 'position', 'city_from'))
                      for user in users]
        }, 200

    def post(self):
        if not current_user.is_admin():
            abort(403, error='Permission denied', message='Требуются права администратора')

        args = user_parser().parse_args()

        existing = db.session.query(User).filter(User.email == args['email']).first()
        if existing:
            abort(400, error='Email already exists', message='Пользователь с таким email уже существует')

        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args.get('age'),
            position=args.get('position'),
            speciality=args.get('speciality'),
            address=args.get('address'),
            email=args['email'],
            active=args.get('active', True),
            city_from=args.get('city_from'),
            fs_uniquifier=str(uuid.uuid4())
        )

        user.set_password(args['password'])
        db.session.add(user)

        if args.get('roles'):
            roles = db.session.query(Role).filter(Role.id.in_(args['roles'])).all()
            user.roles = roles
        else:
            default_role = db.session.query(Role).filter_by(name='user').first()
            if default_role and default_role not in user.roles:
                user.roles.append(default_role)

        db.session.commit()

        return {
            'id': user.id,
            'email': user.email,
            'success': 'User created',
            'message': 'Пользователь успешно создан'
        }, 201


class UsersResource(Resource):
    method_decorators = [login_required]

    def get(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404, error='User not found', message=f'Пользователь с id {user_id} не найден')

        if not (current_user.is_admin() or current_user.id == user_id):
            abort(403, error='Permission denied', message='Доступ запрещен')

        return {'user': user.to_dict()}, 200

    def put(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404, error='User not found', message=f'Пользователь с id {user_id} не найден')

        if not (current_user.is_admin() or current_user.id == user_id):
            abort(403, error='Permission denied', message='Доступ запрещен')

        args = user_update_parser().parse_args()

        if args.get('surname'):
            user.surname = args['surname']
        if args.get('name'):
            user.name = args['name']
        if args.get('age') is not None:
            user.age = args['age']
        if args.get('position'):
            user.position = args['position']
        if args.get('speciality'):
            user.speciality = args['speciality']
        if args.get('address'):
            user.address = args['address']
        if args.get('city_from'):
            user.city_from = args['city_from']

        if args.get('email'):
            existing = db.session.query(User).filter(
                User.email == args['email'],
                User.id != user_id
            ).first()
            if existing:
                abort(400, error='Email already exists',
                      message='Пользователь с таким email уже существует')
            user.email = args['email']

        if args.get('active') is not None and current_user.is_admin():
            user.active = args['active']

        if args.get('roles') and current_user.is_admin():
            roles = db.session.query(Role).filter(Role.id.in_(args['roles'])).all()
            user.roles = roles

        db.session.commit()

        return {
            'success': 'User updated',
            'message': 'Пользователь успешно обновлен',
            'user': user.to_dict(only=('id', 'surname', 'name', 'email'))
        }, 200

    def delete(self, user_id):
        if not current_user.is_admin():
            abort(403, error='Permission denied', message='Требуются права администратора')

        user = db.session.get(User, user_id)
        if not user:
            abort(404, error='User not found', message=f'Пользователь с id {user_id} не найден')

        if user.id == current_user.id:
            abort(400, error='Cannot delete yourself', message='Нельзя удалить самого себя')

        if user.jobs:
            abort(400, error='User has jobs',
                  message='Нельзя удалить пользователя, у которого есть работы')

        try:
            db.session.delete(user)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            abort(500, error='Delete failed', message=f'Ошибка при удалении: {str(e)}')

        return {
            'success': 'User deleted',
            'message': f'Пользователь {user.surname} {user.name} успешно удален'
        }, 200
