from flask_restful import Resource, reqparse, abort
from flask_login import login_required, current_user
from app import db
from app.models import Task, Category

# Парсер для создания задачи
task_parser = reqparse.RequestParser()
task_parser.add_argument('title', type=str, required=True, help='Title is required')
task_parser.add_argument('description', type=str, default='')
task_parser.add_argument('priority', type=str, default='Средний')
task_parser.add_argument('status', type=str, default='В ожидании')
task_parser.add_argument('due_date', type=str)
task_parser.add_argument('category_id', type=int)


class TaskListResource(Resource):
    @login_required
    def get(self):
        """Получить список задач пользователя"""
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return {'tasks': [task.to_dict() for task in tasks]}

    @login_required
    def post(self):
        """Создать новую задачу"""
        args = task_parser.parse_args()
        task = Task(
            title=args['title'],
            description=args['description'],
            priority=args['priority'],
            status=args['status'],
            due_date=args['due_date'],
            user_id=current_user.id,
            category_id=args['category_id']
        )
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), 201


class TaskResource(Resource):
    @login_required
    def get(self, task_id):
        """Получить задачу по ID"""
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            abort(403, message="You don't have permission to access this task")
        return task.to_dict()

    @login_required
    def put(self, task_id):
        """Обновить задачу"""
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            abort(403, message="You don't have permission to update this task")

        args = task_parser.parse_args()
        task.title = args['title']
        task.description = args['description']
        task.priority = args['priority']
        task.status = args['status']
        task.due_date = args['due_date']
        task.category_id = args['category_id']

        db.session.commit()
        return task.to_dict()

    @login_required
    def delete(self, task_id):
        """Удалить задачу"""
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            abort(403, message="You don't have permission to delete this task")

        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted successfully'}, 200


class CategoryResource(Resource):
    @login_required
    def get(self):
        """Получить категории пользователя"""
        categories = Category.query.filter_by(user_id=current_user.id).all()
        return {'categories': [{
            'id': cat.id,
            'name': cat.name,
            'color': cat.color,
            'task_count': cat.tasks.count()
        } for cat in categories]}