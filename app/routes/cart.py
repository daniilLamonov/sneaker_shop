from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from ..models.product import Product
from ..models.cart import Cart
from ..extensions import db

cart = Blueprint('cart', __name__)

@cart.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'Added {product.name} to your cart.', 'success')
    return redirect(url_for('main.index'))

@cart.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        flash('You are not authorized to remove this item.', 'danger')
        return redirect(url_for('cart.view_cart'))
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from your cart.', 'success')
    return redirect(url_for('cart.view_cart'))
@cart.route('/cart')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

