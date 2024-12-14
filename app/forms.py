from flask_wtf import FlaskForm  # Импорт FlaskForm для создания форм в Flask
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField  # Импорт полей формы (строки, пароль, кнопка и булево)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError  # Импорт валидаторов для проверки данных
from .models.user import User  # Импорт модели пользователя для проверки существующих пользователей

# Форма для регистрации пользователя
class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])  # Поле для имени с обязательной валидацией
    email = StringField('Email', validators=[DataRequired(), Email()])  # Поле для email с обязательной валидацией и проверкой формата email
    password = PasswordField('Password', validators=[DataRequired()])  # Поле для пароля с обязательной валидацией
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  # Поле для подтверждения пароля (должно совпадать с полем password)
    submit = SubmitField('Register')  # Кнопка отправки формы

    # Валидатор для проверки уникальности email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # Ищем пользователя с данным email в базе данных
        if user:  # Если пользователь с таким email существует
            raise ValidationError('Email already registered.')  # Возбуждаем ошибку валидации

# Форма для входа пользователя
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Поле для email с обязательной валидацией и проверкой формата email
    password = PasswordField('Password', validators=[DataRequired()])  # Поле для пароля с обязательной валидацией
    remember = BooleanField('Remember Me')  # Чекбокс для запоминания пользователя при входе
    submit = SubmitField('Log In')  # Кнопка отправки формы
