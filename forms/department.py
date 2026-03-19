from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, Optional
from data.db import db
from data.__all_models import User


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired(), Length(min=2, max=100)])
    chief = IntegerField('ID главы департамента', validators=[DataRequired()])
    email = StringField('Email департамента', validators=[DataRequired(), Email()])
    members = SelectMultipleField('Участники', coerce=int, validators=[Optional()])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.members.choices = [
            (user.id, f"{user.surname} {user.name} ({user.email})")
            for user in db.session.query(User).all()
        ]
