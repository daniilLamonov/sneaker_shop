from ..extensions import db

# Определение модели
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))
    size = db.Column(db.String(10))
    price = db.Column(db.Float)
    image = db.Column(db.String(200))
    stock_quantity = db.Column(db.Integer, default=0) # Количество на складе

