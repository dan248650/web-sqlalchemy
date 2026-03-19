from flask import Blueprint, render_template, redirect, flash, request, abort
from configs.configs import login_required
from data.db import db
from data.__all_models import Jobs, User
from forms.job import JobForm
import datetime
from flask_security import current_user

job_bp = Blueprint('job_bp', __name__, template_folder='templates')


@job_bp.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    form.submit.label.text = 'Добавить работу'

    if form.validate_on_submit():
        team_leader = db.session.query(User).get(form.team_leader.data)
        if not team_leader:
            return render_template('jobs/job.html',
                                   title='Добавление работы',
                                   form=form,
                                   message='Тимлид с таким ID не найден',
                                   action='add')

        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=datetime.datetime.now(),
            is_finished=form.is_finished.data
        )

        db.session.add(job)
        db.session.commit()

        flash('Работа успешно добавлена!', 'success')
        return redirect('/')

    return render_template('jobs/job.html',
                           title='Добавление работы',
                           form=form,
                           action='add')


@job_bp.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    form.submit.label.text = 'Сохранить изменения'

    job = db.session.query(Jobs).get(id)
    if not job:
        abort(404)
    if not current_user.can_edit_job(job):
        flash('У вас нет прав для редактирования этой работы', 'danger')
        return redirect('/')

    if request.method == 'GET':
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished

    if form.validate_on_submit():
        team_leader = db.session.query(User).get(form.team_leader.data)
        if not team_leader:
            return render_template('jobs/job.html',
                                   title='Редактирование работы',
                                   form=form,
                                   message='Тимлид с таким ID не найден',
                                   action='edit',
                                   job_id=id)

        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        db.session.commit()

        flash('Работа успешно обновлена!', 'success')
        return redirect('/')

    return render_template('jobs/job.html',
                           title='Редактирование работы',
                           form=form,
                           action='edit',
                           job_id=id)


@job_bp.route('/delete_job/<int:id>', methods=['POST'])
@login_required
def delete_job(id):
    job = db.session.query(Jobs).get(id)
    if not job:
        abort(404)
    if not current_user.can_edit_job(job):
        flash('У вас нет прав для удаления этой работы', 'danger')
        return redirect('/')

    db.session.delete(job)
    db.session.commit()

    flash('Работа успешно удалена!', 'success')
    return redirect('/')
