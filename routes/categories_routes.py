from flask import Blueprint, render_template, redirect, flash, request, abort
from configs.configs import login_required
from data.db import db
from data.__all_models import Category
from forms.category import CategoryForm
from flask_security import current_user

category_bp = Blueprint('category_bp', __name__, template_folder='templates')


@category_bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if not (current_user.is_admin() or current_user.is_captain()):
        flash('У вас нет прав для добавления категорий', 'danger')
        return redirect('/categories')

    form = CategoryForm()
    form.submit.label.text = 'Добавить категорию'

    if form.validate_on_submit():
        existing = db.session.query(Category).filter_by(name=form.name.data).first()
        if existing:
            return render_template('categories/category.html',
                                   title='Добавление категории',
                                   form=form,
                                   message='Категория с таким названием уже существует',
                                   action='add',
                                   return_url='/categories')

        category = Category(
            name=form.name.data,
            description=form.description.data
        )

        db.session.add(category)
        db.session.commit()

        flash('Категория успешно добавлена!', 'success')
        return redirect('/categories')

    return render_template('categories/category.html',
                           title='Добавление категории',
                           form=form,
                           action='add',
                           return_url='/categories')


@category_bp.route('/edit_category/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    if not (current_user.is_admin() or current_user.is_captain()):
        flash('У вас нет прав для редактирования категорий', 'danger')
        return redirect('/categories')

    form = CategoryForm()
    form.submit.label.text = 'Сохранить изменения'

    category = db.session.query(Category).get(id)
    if not category:
        abort(404)

    if request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description

    if form.validate_on_submit():
        existing = db.session.query(Category).filter(
            Category.name == form.name.data,
            Category.id != id
        ).first()
        if existing:
            return render_template('categories/category.html',
                                   title='Редактирование категории',
                                   form=form,
                                   message='Категория с таким названием уже существует',
                                   action='edit',
                                   category_id=id,
                                   return_url='/categories')

        category.name = form.name.data
        category.description = form.description.data

        db.session.commit()
        flash('Категория успешно обновлена!', 'success')
        return redirect('/categories')

    return render_template('categories/category.html',
                           title='Редактирование категории',
                           form=form,
                           action='edit',
                           category_id=id,
                           return_url='/categories')


@category_bp.route('/delete_category/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    if not (current_user.is_admin() or current_user.is_captain()):
        flash('У вас нет прав для удаления категорий', 'danger')
        return redirect('/categories')

    category = db.session.query(Category).get(id)
    if not category:
        abort(404)

    if category.jobs:
        flash('Нельзя удалить категорию, к которой привязаны работы', 'danger')
        return redirect('/categories')

    db.session.delete(category)
    db.session.commit()

    flash('Категория успешно удалена!', 'success')
    return redirect('/categories')
