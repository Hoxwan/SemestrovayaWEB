# Task Manager - Веб-приложение для управления задачами

## Описание
Task Manager - это веб-приложение на Flask для управления задачами, с REST API и веб-интерфейсом.

## Функциональные возможности
- ✅ Регистрация и аутентификация пользователей
- ✅ Создание, редактирование, удаление задач
- ✅ Категоризация задач
- ✅ Приоритеты и статусы задач
- ✅ RESTful API
- ✅ Веб-интерфейс с Bootstrap
- ✅ Авторизация (Flask-Login)
- ✅ База данных (SQLAlchemy)
- ✅ Миграции (Flask-Migrate)

## Установка и запуск


Установка зависимостей
pip install -r requirements.txt

Инициализация базы данных
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Запуск приложения
flask run

http://localhost:5000