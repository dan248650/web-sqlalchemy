import sqlalchemy
from sqlalchemy import orm
from data.db import db
from data.associations import job_category, job_collaborators


class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    job = sqlalchemy.Column(sqlalchemy.String)

    work_size = sqlalchemy.Column(sqlalchemy.Integer)

    start_date = sqlalchemy.Column(sqlalchemy.Date)
    end_date = sqlalchemy.Column(sqlalchemy.Date)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    user = orm.relationship('User', back_populates='jobs')

    collaborators = orm.relationship(
        'User',
        secondary='job_collaborators',
        back_populates='collaborating_jobs'
    )

    categories = orm.relationship(
        'Category',
        secondary='job_category',
        back_populates='jobs'
    )

    def __repr__(self):
        return f'<Job {self.id}: {self.job}>'
