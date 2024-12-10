from .product import Product
from ..extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    status = db.Column(db.String(50), default='user')



    # DROP database shop;
    # CREATE DATABASE shop;
    # GRANT ALL PRIVILEGES ON DATABASE "shop" to seller;
    # ALTER USER seller CREATEDB;
    # GRANT ALL ON schema public TO seller;
    # GRANT USAGE, CREATE ON SCHEMA public TO seller;

