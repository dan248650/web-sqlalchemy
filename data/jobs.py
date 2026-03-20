import sqlalchemy
from sqlalchemy import orm
from data.db import db
from data.associations import job_category, job_collaborators
from sqlalchemy_serializer import SerializerMixin


class Jobs(db.Model, SerializerMixin):
    __tablename__ = 'jobs'

    serialize_rules = (
        '-user.jobs',
        '-collaborators.collaborating_jobs',
        '-categories.jobs'
    )

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
