from flask import Blueprint, render_template

from data.__all_models import User, Jobs
from data.db_session import create_session


logs_bp = Blueprint('logs_bp', __name__, template_folder='templates')


@logs_bp.route('/')
def work_log():
    db_sess = create_session()

    jobs = db_sess.query(Jobs)

    return render_template('logs/work_log.html', title='Журнал работ', jobs=jobs)
