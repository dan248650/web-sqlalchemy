from flask import Blueprint, render_template, redirect

from data.__all_models import User
from data.db_session import create_session

from forms.user import RegisterForm


register_bp = Blueprint('register_bp', __name__, template_folder='templates')


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('auth/register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('auth/register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('auth/register.html', title='Регистрация', form=form)
