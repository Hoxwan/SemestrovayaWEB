from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, \
    IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User, Priority, Status


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким именем уже существует.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким email уже существует.')


class TaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    priority = SelectField('Приоритет', choices=[
        (Priority.LOW.value, 'Низкий'),
        (Priority.MEDIUM.value, 'Средний'),
        (Priority.HIGH.value, 'Высокий')
    ], default=Priority.MEDIUM.value)
    status = SelectField('Статус', choices=[
        (Status.PENDING.value, 'В ожидании'),
        (Status.IN_PROGRESS.value, 'В процессе'),
        (Status.COMPLETED.value, 'Завершено')
    ], default=Status.PENDING.value)
    due_date = DateField('Срок выполнения', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Сохранить')


class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired(), Length(min=1, max=64)])
    color = StringField('Цвет (HEX)', default='#3498db', validators=[Length(min=7, max=7)])
    description = TextAreaField('Описание', validators=[Length(max=200)])
    submit = SubmitField('Создать')


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить изменения')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Пользователь с таким именем уже существует.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Пользователь с таким email уже существует.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new_password2 = PasswordField('Повторите новый пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Изменить пароль')