from flask import Blueprint, render_template, redirect, flash, abort
from flask_security import current_user
from data.db import db
from data.__all_models import User, Jobs, Department, Category

logs_bp = Blueprint('logs_bp', __name__, template_folder='templates')

LOG_CONFIGS = {
    'jobs': {
        'title': 'Журнал работ',
        'model': Jobs,
        'add_url': '/add_job',
        'add_button': 'Добавить работу',
        'edit_url': '/edit_job',
        'delete_url': '/delete_job',
        'empty_message': 'Работ пока нет',
        'item_title_prefix': 'Работа',
        'table_headers': ['Название работы', 'Ответственный', 'Часы', 'Команда', 'Категории', 'Завершена'],
        'can_add': lambda: current_user.is_authenticated,
        'can_edit': lambda job: current_user.is_authenticated and current_user.can_edit_job(job),
        'item_fields': lambda job: [
            job.job,
            f"{job.user.surname} {job.user.name}",
            str(job.work_size),
            ', '.join([f"{u.surname} {u.name}" for u in job.collaborators]) or 'Нет участников',
            ', '.join([cat.name for cat in job.categories]) or 'Нет категорий',
            '<span style="color: #28a745; font-weight: bold;">Завершена</span>' if job.is_finished
            else '<span style="color: #dc3545; font-weight: bold;">Не завершена</span>'
        ]
    },

    'departments': {
        'title': 'Журнал департаментов',
        'model': Department,
        'add_url': '/add_department',
        'add_button': 'Добавить департамент',
        'edit_url': '/edit_department',
        'delete_url': '/delete_department',
        'empty_message': 'Департаментов пока нет',
        'item_title_prefix': 'Департамент',
        'table_headers': ['Название', 'Глава', 'Email', 'Участники'],
        'can_add': lambda: current_user.is_authenticated and (current_user.is_admin() or current_user.is_captain()),
        'can_edit': lambda dept: current_user.is_authenticated and (
                current_user.is_admin() or
                current_user.is_captain() or
                dept.chief == current_user.id
        ),
        'item_fields': lambda dept: [
            dept.title,
            f"{dept.chief_user.surname} {dept.chief_user.name}",
            dept.email,
            ', '.join([f"{m.surname} {m.name}" for m in dept.members]) or 'Нет участников'
        ]
    },

    'users': {
        'title': 'Журнал пользователей',
        'model': User,
        'add_url': None,
        'add_button': None,
        'edit_url': '/edit_user',
        'delete_url': '/delete_user',
        'empty_message': 'Пользователей пока нет',
        'item_title_prefix': 'Пользователь',
        'table_headers': ['Фамилия', 'Имя', 'Возраст', 'Должность', 'Специальность', 'Email', 'Роли'],
        'can_add': lambda: False,
        'can_edit': lambda user: current_user.is_authenticated and current_user.is_admin(),
        'item_fields': lambda user: [
            user.surname,
            user.name,
            str(user.age),
            user.position,
            user.speciality,
            user.email,
            ', '.join([role.name for role in user.roles]) or 'Нет ролей'
        ]
    },

    'categories': {
        'title': 'Журнал категорий',
        'model': Category,
        'add_url': '/add_category',
        'add_button': 'Добавить категорию',
        'edit_url': '/edit_category',
        'delete_url': '/delete_category',
        'empty_message': 'Категорий пока нет',
        'item_title_prefix': 'Категория',
        'table_headers': ['Название', 'Описание', 'Количество работ'],
        'can_add': lambda: current_user.is_authenticated and (
                current_user.is_admin() or current_user.is_captain()),
        'can_edit': lambda cat: current_user.is_authenticated and (
                current_user.is_admin() or current_user.is_captain()),
        'item_fields': lambda cat: [
            cat.name,
            cat.description or 'Нет описания',
            str(len(cat.jobs))
        ]
    }
}


def render_log(log_type):
    config = LOG_CONFIGS.get(log_type)
    if not config:
        abort(404)

    if log_type == 'users' and not current_user.is_admin():
        flash('У вас нет прав для просмотра пользователей', 'danger')
        return redirect('/')

    items = db.session.query(config['model']).all()

    return render_template('logs/base_log.html',
                           log_title=config['title'],
                           items=items,
                           can_add=config['can_add'](),
                           add_url=config['add_url'],
                           add_button_text=config['add_button'],
                           can_edit=config['can_edit'],
                           edit_url=config['edit_url'],
                           delete_url=config['delete_url'],
                           delete_confirm_message='Вы уверены, что хотите удалить этот элемент?',
                           item_title_prefix=config['item_title_prefix'],
                           table_headers=config['table_headers'],
                           item_fields=config['item_fields'],
                           empty_message=config['empty_message'])


@logs_bp.route('/')
def work_log():
    return render_log('jobs')


@logs_bp.route('/departments')
def departments_log():
    return render_log('departments')


@logs_bp.route('/users')
def users_log():
    return render_log('users')


@logs_bp.route('/categories')
def categories_log():
    return render_log('categories')
