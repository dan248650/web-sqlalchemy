from flask import Blueprint, render_template, redirect, flash
from configs.configs import login_required
from data.db import db
from data.__all_models import Jobs, User
from forms.job import JobForm
import datetime

job_bp = Blueprint('job_bp', __name__, template_folder='templates')


@job_bp.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()

    if form.validate_on_submit():
        team_leader = db.session.query(User).get(form.team_leader.data)
        if not team_leader:
            return render_template('jobs/job.html',
                                   title='Добавление работы',
                                   form=form,
                                   message='Тимлид с таким ID не найден')

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

    return render_template('jobs/job.html', title='Добавление работы', form=form)
