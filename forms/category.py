from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired(), Length(min=2, max=50)])
    description = StringField('Описание', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Сохранить')
