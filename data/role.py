import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from data.associations import user_role


class Role(SqlAlchemyBase):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    users = orm.relationship('User', secondary='user_role', back_populates='roles')
