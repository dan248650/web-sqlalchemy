import sqlalchemy
from sqlalchemy import orm
from data.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from data.associations import user_role, department_members, job_collaborators
from datetime import datetime
from flask_security import UserMixin
from sqlalchemy import event
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = (
        '-hashed_password',
        '-fs_uniquifier',
        '-jobs.user',
        '-jobs.collaborators',
        '-jobs.categories',
        '-collaborating_jobs.collaborators',
        '-collaborating_jobs.user',
        '-collaborating_jobs.categories',
        '-chief_of_departments.chief_user',
        '-chief_of_departments.members',
        '-member_of_departments.members',
        '-member_of_departments.chief_user',
        '-roles.users',
    )

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    city_from = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    fs_uniquifier = sqlalchemy.Column(sqlalchemy.String, unique=True)

    jobs = orm.relationship('Jobs', back_populates='user')
    roles = orm.relationship('Role', secondary='user_role', back_populates='users')

    chief_of_departments = orm.relationship(
        'Department',
        foreign_keys='Department.chief',
        back_populates='chief_user'
    )

    member_of_departments = orm.relationship(
        'Department',
        secondary='department_members',
        back_populates='members'
    )

    collaborating_jobs = orm.relationship(
        'Jobs',
        secondary='job_collaborators',
        back_populates='collaborators'
    )

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_captain(self):
        return any(role.name == 'captain' for role in self.roles)

    def is_admin(self):
        return any(role.name == 'admin' for role in self.roles)

    def can_edit_job(self, job):
        if self.is_admin():
            return True
        if self.is_captain():
            return True
        if job.team_leader == self.id:
            return True
        return False

    def __repr__(self):
        return f'<User {self.id}: {self.name} {self.surname}>'


@event.listens_for(User, 'after_insert')
def add_default_role(mapper, connection, target):
    from data.__all_models import Role

    role = connection.execute(
        Role.__table__.select().where(Role.name == 'user')
    ).first()

    if role:
        connection.execute(
            user_role.insert().values(
                user_id=target.id,
                role_id=role.id
            )
        )
