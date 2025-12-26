import pytest
import json
from app import create_app, db
from app.models import User, Task


@pytest.fixture
def app():
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    # Создание тестового пользователя
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')

    with client.application.app_context():
        db.create_all()
        db.session.add(user)
        db.session.commit()

    # Аутентификация
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    })

    return client


def test_api_tasks_get(auth_client):
    response = auth_client.get('/api/tasks')
    assert response.status_code == 200
    assert 'tasks' in json.loads(response.data)


def test_api_task_create(auth_client):
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 'Средний',
        'status': 'В ожидании'
    }

    response = auth_client.post('/api/tasks', json=task_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'


def test_api_task_update(auth_client):
    # Сначала создаем задачу
    task_data = {'title': 'Test Task'}
    response = auth_client.post('/api/tasks', json=task_data)
    task_id = json.loads(response.data)['id']

    # Обновляем задачу
    update_data = {'title': 'Updated Task'}
    response = auth_client.put(f'/api/tasks/{task_id}', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Task'


def test_api_task_delete(auth_client):
    # Создаем задачу для удаления
    task_data = {'title': 'Task to Delete'}
    response = auth_client.post('/api/tasks', json=task_data)
    task_id = json.loads(response.data)['id']

    # Удаляем задачу
    response = auth_client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200