import sqlalchemy
from data.db_session import SqlAlchemyBase

user_role = sqlalchemy.Table(
    'user_role',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('role_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'))
)
