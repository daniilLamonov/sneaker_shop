from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required

from ..functions import save_picture
from ..extensions import db
from ..models.product import Product

product = Blueprint('product', __name__)

@product.route('/products/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        color = request.form.get('color')
        size = request.form.get('size')
        image_file = save_picture(request.files.get('image'))

        product = Product(name=name, price=price, color=color, size=size, image=image_file)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            flash(f'Something went wrong!{str(e)}', category='error')
            return redirect('/')
    else:
        return render_template('product/create.html')

@product.route('/product/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.color = request.form.get('color')
        product.size = request.form.get('size')
        product.image = request.files.get('image')

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            flash(f'Something went wrong!{str(e)}', category='error')
            return redirect('/')
    else:
        return render_template('/product/edit.html', product=product)

@product.route('/products/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    product = Product.query.get(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(str(e))