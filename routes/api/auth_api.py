from flask import jsonify, request, make_response
from flask_security import login_user, logout_user, current_user
from data.db import db
from data.__all_models import User
from configs.configs import login_required
from . import api_bp


@api_bp.route('/login', methods=['POST'])
def api_login():
    """API авторизация"""
    if current_user.is_authenticated:
        return jsonify({
            'message': 'Already logged in',
            'user': current_user.to_dict(only=['id', 'name', 'surname', 'email', 'roles'])
        })

    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return make_response(jsonify({'error': 'Email and password required'}), 400)

    user = db.session.query(User).filter(User.email == email).first()

    if user and user.check_password(password):
        if not user.active:
            return make_response(jsonify({'error': 'Account is deactivated'}), 403)

        login_user(user, remember=request.json.get('remember', False))

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict(only=['id', 'name', 'surname', 'email', 'roles'])
        })
    else:
        return make_response(jsonify({'error': 'Invalid email or password'}), 401)


@api_bp.route('/logout', methods=['POST'])
@login_required
def api_logout():
    """API выход из системы"""
    logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@api_bp.route('/me', methods=['GET'])
@login_required
def api_me():
    """Получить информацию о текущем пользователе"""
    return jsonify({
        'user': current_user.to_dict()
    })
