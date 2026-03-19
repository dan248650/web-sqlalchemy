import sqlalchemy
from sqlalchemy import orm
from data.db import db
from data.associations import job_category


class Category(db.Model):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    jobs = orm.relationship(
        'Jobs',
        secondary='job_category',
        back_populates='categories'
    )
