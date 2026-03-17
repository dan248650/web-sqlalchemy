import sqlalchemy
from data.db_session import SqlAlchemyBase

user_role = sqlalchemy.Table(
    'user_role',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('role_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'))
)

department_members = sqlalchemy.Table(
    'department_members',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('department_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('departments.id')),
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
)
