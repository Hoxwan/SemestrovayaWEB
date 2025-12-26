from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.main import main_bp
from app.models import Task, Category, Priority, Status
from app.forms import TaskForm, CategoryForm
from datetime import datetime
from sqlalchemy import or_


@main_bp.route('/')
@main_bp.route('/index')
def index():
    if current_user.is_authenticated:
        # Статистика
        total_tasks = Task.query.filter_by(user_id=current_user.id).count()
        completed_tasks = Task.query.filter_by(user_id=current_user.id, status=Status.COMPLETED).count()

        # Последние 5 задач
        recent_tasks = Task.query.filter_by(user_id=current_user.id) \
            .order_by(Task.created_at.desc()) \
            .limit(5) \
            .all()

        return render_template('index.html',
                               total_tasks=total_tasks,
                               completed_tasks=completed_tasks,
                               recent_tasks=recent_tasks)
    return render_template('index.html')


@main_bp.route('/tasks')
@login_required
def tasks():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '')

    query = Task.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f'%{search}%'),
                Task.description.ilike(f'%{search}%')
            )
        )

    if status_filter == 'completed':
        query = query.filter_by(status=Status.COMPLETED)
    elif status_filter == 'pending':
        query = query.filter_by(status=Status.PENDING)
    elif status_filter == 'in_progress':
        query = query.filter_by(status=Status.IN_PROGRESS)

    tasks = query.order_by(Task.created_at.desc()) \
        .paginate(page=page, per_page=10, error_out=False)

    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template('tasks.html',
                           tasks=tasks,
                           status_filter=status_filter,
                           search=search,
                           categories=categories,
                           datetime=datetime)


@main_bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=Priority(form.priority.data),
            status=Status(form.status.data),
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Задача успешно создана!', 'success')
        return redirect(url_for('main.tasks'))

    return render_template('task_form.html',
                           title='Новая задача',
                           form=form,
                           action_url=url_for('main.new_task'))


@main_bp.route('/task/<int:id>')
@login_required
def view_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('У вас нет доступа к этой задаче', 'danger')
        return redirect(url_for('main.tasks'))

    return render_template('task_detail.html', task=task)


@main_bp.route('/task/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('У вас нет прав для редактирования этой задачи', 'danger')
        return redirect(url_for('main.tasks'))

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = Priority(form.priority.data)
        task.status = Status(form.status.data)
        task.due_date = form.due_date.data
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Задача успешно обновлена!', 'success')
        return redirect(url_for('main.tasks'))

    return render_template('task_form.html',
                           title='Редактировать задачу',
                           form=form,
                           action_url=url_for('main.edit_task', id=id))


@main_bp.route('/task/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('У вас нет прав для удаления этой задачи', 'danger')
        return redirect(url_for('main.tasks'))

    db.session.delete(task)
    db.session.commit()
    flash('Задача успешно удалена!', 'success')
    return redirect(url_for('main.tasks'))


@main_bp.route('/task/<int:id>/complete', methods=['POST'])
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'Нет прав'}), 403

    task.status = Status.COMPLETED
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})


@main_bp.route('/categories')
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form = CategoryForm()
    return render_template('categories.html', categories=categories, form=form)


@main_bp.route('/category/new', methods=['POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            color=form.color.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Категория успешно создана!', 'success')
    else:
        flash('Ошибка при создании категории', 'danger')
    return redirect(url_for('main.categories'))


@main_bp.route('/category/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('У вас нет прав для удаления этой категории', 'danger')
        return redirect(url_for('main.categories'))

    db.session.delete(category)
    db.session.commit()
    flash('Категория успешно удалена!', 'success')
    return redirect(url_for('main.categories'))