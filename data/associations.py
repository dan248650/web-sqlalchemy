from data.db import db


user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


department_members = db.Table('department_members',
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


job_category = db.Table('job_category',
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)
