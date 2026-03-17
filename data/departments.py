import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from data.associations import department_members


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    chief_user = orm.relationship('User', foreign_keys=[chief])

    members = orm.relationship(
        'User',
        secondary='department_members',
        back_populates='member_of_departments'
    )
