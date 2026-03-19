from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from data.db import db
from data.__all_models import Category


class JobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('ID тимлида', validators=[DataRequired(), NumberRange(min=1)])
    work_size = IntegerField('Продолжительность (часы)', validators=[DataRequired(), NumberRange(min=1)])
    collaborators = StringField('ID участников (через запятую)', validators=[DataRequired()])
    categories = SelectMultipleField('Категории', coerce=int)
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Добавить работу')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories.choices = [
            (cat.id, f"{cat.name} - {cat.description}")
            for cat in db.session.query(Category).all()
        ]
