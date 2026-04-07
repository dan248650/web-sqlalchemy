from flask_restful import reqparse


def job_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('job', type=str, required=True, help='Название работы')
    parser.add_argument('team_leader', type=int, required=True, help='ID руководителя')
    parser.add_argument('work_size', type=int, required=True, help='Объем работы')

    parser.add_argument('start_date', type=str, required=False, help='Дата начала (YYYY-MM-DD)')
    parser.add_argument('end_date', type=str, required=False, help='Дата окончания (YYYY-MM-DD)')
    parser.add_argument('is_finished', type=bool, required=False, help='Завершена ли работа')
    parser.add_argument('collaborators', type=list, location='json', required=False, help='Список ID участников')
    parser.add_argument('categories', type=list, location='json', required=False, help='Список ID категорий')

    return parser


def job_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('job', type=str, required=False, help='Название работы')
    parser.add_argument('team_leader', type=int, required=False, help='ID руководителя')
    parser.add_argument('work_size', type=int, required=False, help='Объем работы')
    parser.add_argument('start_date', type=str, required=False, help='Дата начала (YYYY-MM-DD)')
    parser.add_argument('end_date', type=str, required=False, help='Дата окончания (YYYY-MM-DD)')
    parser.add_argument('is_finished', type=bool, required=False, help='Завершена ли работа')
    parser.add_argument('collaborators', type=list, location='json', required=False, help='Список ID участников')
    parser.add_argument('categories', type=list, location='json', required=False, help='Список ID категорий')

    return parser
