from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user

from ..forms import RegistrationForm, LoginForm  # Импорт форм регистрации и входа
from ..models.user import User  # Импорт модели пользователя
from ..extensions import db, bcrypt  # Импорт базы данных и bcrypt для хэширования паролей

user = Blueprint('user', __name__)  # Создаем Blueprint для пользовательских маршрутов

# Маршрут для регистрации нового пользователя
@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Инициализация формы регистрации
    if form.validate_on_submit():  # Проверка, прошла ли форма валидацию при отправке
        # Хэшируем пароль перед сохранением в базу данных
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)  # Создаем нового пользователя
        try:
            db.session.add(user)  # Добавляем пользователя в сессию базы данных
            db.session.commit()  # Сохраняем изменения в базе данных
            flash('Your account has been created! You are now able to login', 'success')  # Сообщение об успешной регистрации
            return redirect(url_for('user.login'))  # Перенаправление на страницу входа
        except Exception as e:  # Обработка ошибок при добавлении пользователя
            print(e)  # Логирование ошибки (можно заменить на более продвинутую обработку)
            flash('There was an error creating your account', 'danger')  # Сообщение об ошибке
    return render_template('user/register.html', form=form)  # Отправка формы на страницу регистрации


# Маршрут для входа пользователя
@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Инициализация формы входа
    if form.validate_on_submit():  # Проверка, прошла ли форма валидацию при отправке
        user = User.query.filter_by(email=form.email.data).first()  # Поиск пользователя по email
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # Проверка правильности пароля
            login_user(user, remember=form.remember.data)  # Вход пользователя в систему с опцией "Запомнить"
            next_page = request.args.get('next')  # Получаем страницу, на которую нужно перенаправить после входа
            flash('You are now logged in', 'success')  # Сообщение об успешном входе
            return redirect(next_page) if next_page else redirect(url_for('main.index'))  # Перенаправление либо на запрашиваемую страницу, либо на главную
        else:
            flash('Login failed.', 'danger')  # Сообщение об ошибке при неверных данных для входа
    return render_template('user/login.html', form=form)  # Отправка формы на страницу входа
# Маршрут для выхода пользователя
@user.route('/user/logout')
def logout():
    logout_user()  # Выход пользователя из системы
    return redirect(url_for('main.index'))  # Перенаправление на главную страницу
