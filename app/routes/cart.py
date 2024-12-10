from flask import Blueprint, render_template

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def open_cart():
    return render_template('main/cart.html')