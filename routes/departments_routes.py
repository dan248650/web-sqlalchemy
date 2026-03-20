from flask import Blueprint, render_template, redirect, flash, request, abort
from configs.configs import login_required
from data.db import db
from data.__all_models import Department, User
from forms.department import DepartmentForm
from flask_security import current_user

department_bp = Blueprint('department_bp', __name__, template_folder='templates')


@department_bp.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    if not (current_user.is_admin() or current_user.is_captain()):
        flash('У вас нет прав для добавления департаментов', 'danger')
        return redirect('/departments')

    form = DepartmentForm()
    form.submit.label.text = 'Добавить департамент'

    if form.validate_on_submit():
        chief = db.session.query(User).get(form.chief.data)
        if not chief:
            return render_template('departments/department.html',
                                   title='Добавление департамента',
                                   form=form,
                                   message='Глава с таким ID не найден',
                                   action='add',
                                   return_url='/departments')

        existing = db.session.query(Department).filter_by(email=form.email.data).first()
        if existing:
            return render_template('departments/department.html',
                                   title='Добавление департамента',
                                   form=form,
                                   message='Департамент с таким email уже существует',
                                   action='add',
                                   return_url='/departments')

        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            email=form.email.data
        )

        db.session.add(department)

        if form.members.data:
            members = db.session.query(User).filter(User.id.in_(form.members.data)).all()
            department.members = members

        db.session.commit()

        flash('Департамент успешно добавлен!', 'success')
        return redirect('/departments')

    return render_template('departments/department.html',
                           title='Добавление департамента',
                           form=form,
                           action='add',
                           return_url='/departments')


@department_bp.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    department = db.session.query(Department).get(id)
    if not department:
        abort(404)

    if not (current_user.is_admin() or current_user.is_captain() or
            current_user.id == department.chief):
        flash('У вас нет прав для редактирования этого департамента', 'danger')
        return redirect('/departments')

    form = DepartmentForm()
    form.submit.label.text = 'Сохранить изменения'

    if request.method == 'GET':
        form.title.data = department.title
        form.chief.data = department.chief
        form.email.data = department.email
        form.members.data = [m.id for m in department.members]

    if form.validate_on_submit():
        chief = db.session.query(User).get(form.chief.data)
        if not chief:
            return render_template('departments/department.html',
                                   title='Редактирование департамента',
                                   form=form,
                                   message='Глава с таким ID не найден',
                                   action='edit',
                                   department_id=id,
                                   return_url='/departments')

        existing = db.session.query(Department).filter(
            Department.email == form.email.data,
            Department.id != id
        ).first()
        if existing:
            return render_template('departments/department.html',
                                   title='Редактирование департамента',
                                   form=form,
                                   message='Департамент с таким email уже существует',
                                   action='edit',
                                   department_id=id,
                                   return_url='/departments')

        department.title = form.title.data
        department.chief = form.chief.data
        department.email = form.email.data

        if form.members.data:
            members = db.session.query(User).filter(User.id.in_(form.members.data)).all()
            department.members = members
        else:
            department.members = []

        db.session.commit()
        flash('Департамент успешно обновлен!', 'success')
        return redirect('/departments')

    return render_template('departments/department.html',
                           title='Редактирование департамента',
                           form=form,
                           action='edit',
                           department_id=id,
                           return_url='/departments')


@department_bp.route('/delete_department/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    if not (current_user.is_admin() or current_user.is_captain()):
        flash('У вас нет прав для удаления департаментов', 'danger')
        return redirect('/departments')

    department = db.session.query(Department).get(id)
    if not department:
        abort(404)

    db.session.delete(department)
    db.session.commit()

    flash('Департамент успешно удален!', 'success')
    return redirect('/departments')
