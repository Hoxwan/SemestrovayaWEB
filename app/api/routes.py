from app.api import api, api_bp
from app.api.resources import TaskListResource, TaskResource, CategoryResource

# Регистрация ресурсов API
api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')
api.add_resource(CategoryResource, '/categories')

@api_bp.route('/')
def api_index():
    return {
        'message': 'Task Manager API',
        'version': '1.0',
        'endpoints': {
            'tasks': '/api/tasks',
            'task': '/api/tasks/<id>',
            'categories': '/api/categories'
        }
    }