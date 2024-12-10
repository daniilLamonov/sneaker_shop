from flask import Flask
from .extensions import db, migrate, login_manager
from .config import (Config)
from .routes.product import product
from .routes.main import main
from .routes.cart import cart
from .routes.user import user

def create_app(config_name=Config):
    # Создание приложения Flask
    app = Flask(__name__)

    # Регистрируем Blueprint
    app.register_blueprint(main)
    app.register_blueprint(cart)
    app.register_blueprint(user)
    app.register_blueprint(product)

    # Конфигурация базы данных
    app.config.from_object(config_name)

    # Инициализирует объект db (SQLAlchemy) с текущим экземпляром приложения Flask.
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # LOGIN_MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'

    # Создание базы данных
    with app.app_context():
        db.create_all()  # Создаёт таблицы в базе данных на основе определённых моделей
    return app