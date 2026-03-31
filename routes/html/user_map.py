from flask import render_template, Blueprint, abort, redirect, flash, url_for
from flask_security import current_user
from data.db import db
from data.__all_models import User
from utils.map_utils import get_coordinates, get_map_params
import requests
import traceback

user_map_bp = Blueprint('user_map', __name__, template_folder='templates')


@user_map_bp.route('/users_show/<int:user_id>')
def show_user_map(user_id):
    if not current_user.is_authenticated:
        flash('Необходимо войти в систему', 'warning')
        return redirect(url_for('login_bp.login'))

    try:
        from configs.configs import app
        with app.app_context():
            user = db.session.get(User, user_id)
            if not user:
                abort(404, description="Пользователь не найден")

            if not (current_user.is_admin() or current_user.id == user_id):
                abort(403, description="Доступ запрещен")

            if not user.city_from:
                abort(404, description="Город не указан для этого колониста")

            city_name = user.city_from
            full_name = f"{user.surname} {user.name}"

            api_key = app.config.get('YANDEX_MAPS_API_KEY', '')
            if not api_key:
                abort(500, description="API ключ Яндекс.Карт не настроен")

            coordinates = get_coordinates(city_name, api_key)
            if not coordinates:
                abort(404, description=f"Город '{city_name}' не найден на карте")

            lon, lat = coordinates
            points = [{
                "coords": f"{lon},{lat}",
                "style": "pm2rdl"
            }]

            map_type = "sat"
            map_params = get_map_params(points, map_type=map_type)
            static_map_url = f"https://static-maps.yandex.ru/1.x/?{requests.compat.urlencode(map_params)}"

            return render_template(
                'users/user_map.html',
                title=f"Карта: {city_name} - {full_name}",
                city_name=city_name,
                user_name=full_name,
                user_id=user_id,
                static_map_url=static_map_url,
                lon=lon,
                lat=lat
            )

    except Exception as e:
        print(f"Ошибка: {e}")
        print(traceback.format_exc())
        abort(500, description=f"Ошибка при получении данных: {str(e)}")
