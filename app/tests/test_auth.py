import pytest
from app.models import User


def test_register(client):
    """Тест регистрации пользователя"""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Регистрация прошла успешно' in response.data

    # Проверяем, что пользователь создан в базе
    with client.application.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'


def test_login(client):
    """Тест входа пользователя"""
    # Сначала создаем пользователя
    with client.application.app_context():
        user = User(username='loginuser', email='login@example.com')
        user.set_password('mypassword')
        db.session.add(user)
        db.session.commit()

    # Пытаемся войти
    response = client.post('/auth/login', data={
        'username': 'loginuser',
        'password': 'mypassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Добро пожаловать' in response.data


def test_invalid_login(client):
    """Тест неверного входа"""
    response = client.post('/auth/login', data={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    })

    assert response.status_code == 200
    assert b'Неверное имя пользователя или пароль' in response.data


def test_logout(authenticated_client):
    """Тест выхода из системы"""
    response = authenticated_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Вы успешно вышли из системы' in response.data