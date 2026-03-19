import sqlalchemy
from sqlalchemy import orm
from data.db import db
from data.associations import job_category


class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    job = sqlalchemy.Column(sqlalchemy.String)

    work_size = sqlalchemy.Column(sqlalchemy.Integer)

    collaborators = sqlalchemy.Column(sqlalchemy.String)

    start_date = sqlalchemy.Column(sqlalchemy.Date)
    end_date = sqlalchemy.Column(sqlalchemy.Date)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)

    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User', back_populates='jobs')

    categories = orm.relationship(
        'Category',
        secondary='job_category',
        back_populates='jobs'
    )
