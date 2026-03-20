import sqlalchemy
from sqlalchemy import orm
from data.db import db
from data.associations import department_members
from sqlalchemy_serializer import SerializerMixin


class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    serialize_rules = (
        '-chief_user.chief_of_departments',
        '-chief_user.member_of_departments',
        '-chief_user.jobs',
        '-chief_user.collaborating_jobs',
        '-chief_user.roles',
        '-members.member_of_departments',
        '-members.chief_of_departments',
        '-members.jobs',
        '-members.collaborating_jobs',
        '-members.roles',
    )

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    chief_user = orm.relationship('User', foreign_keys=[chief], back_populates='chief_of_departments')

    members = orm.relationship(
        'User',
        secondary='department_members',
        back_populates='member_of_departments'
    )

    def __repr__(self):
        return f'<Department {self.id}: {self.title}>'
