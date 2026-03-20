import sqlalchemy
from sqlalchemy import orm
from data.db import db
from data.associations import job_category
from sqlalchemy_serializer import SerializerMixin


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    serialize_rules = (
        '-jobs.categories',
        '-jobs.user',
        '-jobs.collaborators',
    )

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    jobs = orm.relationship(
        'Jobs',
        secondary='job_category',
        back_populates='categories'
    )

    def __repr__(self):
        return f'<Category {self.id}: {self.name}>'
