from flask import jsonify, request, make_response
from flask_security import current_user
from routes.api import api_bp
from data.db import db
from data.__all_models import User, Role
from configs.configs import login_required
import uuid


@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """Получить список всех пользователей"""
    if not current_user.is_admin():
        return make_response(jsonify({'error': 'Permission denied'}), 403)

    users = db.session.query(User).all()
    return jsonify({
        'users': [user.to_dict(only=('id', 'surname', 'name', 'email', 'position'))
                  for user in users]
    })


@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Получить одного пользователя"""
    user = db.session.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    if not (current_user.is_admin() or current_user.id == user_id):
        return make_response(jsonify({'error': 'Permission denied'}), 403)

    return jsonify({
        'user': user.to_dict()
    })


@api_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    """Создать нового пользователя"""
    if not current_user.is_admin():
        return make_response(jsonify({'error': 'Permission denied'}), 403)

    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    required_fields = ['surname', 'name', 'email', 'password']
    if not all(field in request.json for field in required_fields):
        return make_response(jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400)

    existing = db.session.query(User).filter(
        User.email == request.json['email']
    ).first()
    if existing:
        return make_response(jsonify({'error': 'Email already exists'}), 400)

    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json.get('age'),
        position=request.json.get('position'),
        speciality=request.json.get('speciality'),
        address=request.json.get('address'),
        email=request.json['email'],
        active=request.json.get('active', True),
        fs_uniquifier=str(uuid.uuid4())
    )

    db.session.add(user)

    user.set_password(request.json['password'])

    if 'roles' in request.json and request.json['roles']:
        roles = db.session.query(Role).filter(
            Role.id.in_(request.json['roles'])
        ).all()
        user.roles = roles
    else:
        default_role = db.session.query(Role).filter_by(name='user').first()
        if default_role:
            user.roles.append(default_role)

    db.session.commit()

    return jsonify({
        'id': user.id,
        'email': user.email,
        'success': 'User created'
    }), 201


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """Обновить пользователя"""
    user = db.session.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    if not (current_user.is_admin() or current_user.id == user_id):
        return make_response(jsonify({'error': 'Permission denied'}), 403)

    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        existing = db.session.query(User).filter(
            User.email == request.json['email'],
            User.id != user_id
        ).first()
        if existing:
            return make_response(jsonify({'error': 'Email already exists'}), 400)
        user.email = request.json['email']
    if 'active' in request.json and current_user.is_admin():
        user.active = request.json['active']
    if 'roles' in request.json and current_user.is_admin():
        roles = db.session.query(Role).filter(Role.id.in_(request.json['roles'])).all()
        user.roles = roles

    db.session.commit()
    return jsonify({'success': 'User updated'})


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Удалить пользователя"""
    if not current_user.is_admin():
        return make_response(jsonify({'error': 'Permission denied'}), 403)

    user = db.session.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    if user.id == current_user.id:
        return make_response(jsonify({'error': 'Cannot delete yourself'}), 400)

    if user.jobs:
        return make_response(jsonify({'error': 'User has jobs'}), 400)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': 'User deleted'})
