from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class JobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('ID тимлида', validators=[DataRequired(), NumberRange(min=1)])
    work_size = IntegerField('Продолжительность (часы)', validators=[DataRequired(), NumberRange(min=1)])
    collaborators = StringField('ID участников (через запятую)', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Добавить работу')
