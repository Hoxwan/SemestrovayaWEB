import pytest
from app import create_app, db
from app.models import User


@pytest.fixture(scope='module')
def app():
    """Фикстура для создания приложения"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    """Фикстура для тестового клиента"""
    return app.test_client()


@pytest.fixture(scope='module')
def runner(app):
    """Фикстура для тестового клик-раннера"""
    return app.test_cli_runner()


@pytest.fixture(scope='module')
def authenticated_client(client):
    """Фикстура для аутентифицированного клиента"""
    # Создание тестового пользователя
    with client.application.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            is_admin=False
        )
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    # Авторизация
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    return client