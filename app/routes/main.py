from tempfile import template

from flask import Blueprint, render_template

from ..models.product import Product

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    products = Product.query.all()

    return render_template('main/index.html', products=products)