from flask_restful import reqparse


def user_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('surname', type=str, required=True, help='Фамилия пользователя')
    parser.add_argument('name', type=str, required=True, help='Имя пользователя')
    parser.add_argument('email', type=str, required=True, help='Email пользователя')
    parser.add_argument('password', type=str, required=True, help='Пароль пользователя')

    parser.add_argument('age', type=int, required=False, help='Возраст пользователя')
    parser.add_argument('position', type=str, required=False, help='Должность пользователя')
    parser.add_argument('speciality', type=str, required=False, help='Специализация пользователя')
    parser.add_argument('address', type=str, required=False, help='Адрес пользователя')
    parser.add_argument('city_from', type=str, required=False, help='Родной город пользователя')
    parser.add_argument('active', type=bool, required=False, help='Активен ли пользователь')
    parser.add_argument('roles', type=list, location='json', required=False, help='Список ID ролей')

    return parser


def user_update_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('surname', type=str, required=False, help='Фамилия пользователя')
    parser.add_argument('name', type=str, required=False, help='Имя пользователя')
    parser.add_argument('age', type=int, required=False, help='Возраст пользователя')
    parser.add_argument('position', type=str, required=False, help='Должность пользователя')
    parser.add_argument('speciality', type=str, required=False, help='Специализация пользователя')
    parser.add_argument('address', type=str, required=False, help='Адрес пользователя')
    parser.add_argument('city_from', type=str, required=False, help='Родной город пользователя')
    parser.add_argument('email', type=str, required=False, help='Email пользователя')
    parser.add_argument('active', type=bool, required=False, help='Активен ли пользователь')
    parser.add_argument('roles', type=list, location='json', required=False, help='Список ID ролей')

    return parser
