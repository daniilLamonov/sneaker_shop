from flask import Blueprint, render_template, request, redirect, flash  # Импортируем необходимые модули из Flask
from flask_login import login_required  # Импортируем декоратор для защиты маршрутов от незалогиненных пользователей

from ..functions import save_picture  # Импортируем функцию для сохранения изображений
from ..extensions import db  # Импортируем объект базы данных для работы с моделями
from ..models.product import Product  # Импортируем модель Product для взаимодействия с товарами в базе данных

# Создаем Blueprint для маршрутов, связанных с продуктами
product = Blueprint('product', __name__)


# Маршрут для создания нового продукта
@product.route('/products/create/', methods=['GET', 'POST'])
@login_required  # Только для авторизованных пользователей
def create():
    if request.method == 'POST':  # Если форма была отправлена методом POST
        # Извлекаем данные из формы
        name = request.form.get('name')
        price = request.form.get('price')
        color = request.form.get('color')
        size = request.form.get('size')

        # Получаем изображение и сохраняем его с помощью функции save_picture
        image_file = save_picture(request.files.get('image'))

        # Создаем новый объект Product и добавляем его в сессию базы данных
        product = Product(name=name, price=price, color=color, size=size, image=image_file)
        try:
            db.session.add(product)  # Добавляем новый продукт в сессию
            db.session.commit()  # Сохраняем изменения в базе данных
            return redirect('/')  # Перенаправляем на главную страницу
        except Exception as e:
            flash(f'Something went wrong!{str(e)}', category='error')  # Показываем сообщение об ошибке
            return redirect('/')  # Перенаправляем на главную страницу
    else:
        return render_template('product/create.html')  # Отображаем форму создания продукта, если запрос GET


# Маршрут для редактирования существующего продукта
@product.route('/product/<int:id>/edit/', methods=['GET', 'POST'])
@login_required  # Только для авторизованных пользователей
def edit(id):
    product = Product.query.get(id)  # Ищем продукт в базе данных по его ID
    if request.method == 'POST':  # Если форма была отправлена методом POST
        # Обновляем данные о продукте
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.color = request.form.get('color')
        product.size = request.form.get('size')

        # Получаем изображение и сохраняем его с помощью функции save_picture
        product.image = save_picture(request.files.get('image'))
        try:
            db.session.commit()  # Сохраняем изменения в базе данных
            return redirect('/')  # Перенаправляем на главную страницу
        except Exception as e:
            flash(f'Something went wrong!{str(e)}', category='error')  # Показываем сообщение об ошибке
            return redirect('/')  # Перенаправляем на главную страницу
    else:
        return render_template('/product/edit.html',
                               product=product)  # Отображаем форму редактирования с текущими данными о продукте


# Маршрут для удаления продукта
@product.route('/products/<int:id>/delete', methods=['GET', 'POST'])
@login_required  # Только для авторизованных пользователей
def delete(id):
    product = Product.query.get(id)  # Ищем продукт в базе данных по его ID
    try:
        db.session.delete(product)  # Удаляем продукт из базы данных
        db.session.commit()  # Сохраняем изменения
        return redirect('/')  # Перенаправляем на главную страницу
    except Exception as e:
        print(str(e))  # Логируем ошибку (можно улучшить обработку ошибок, например, с использованием flash-сообщений)
@product.route('/products/<int:id>/detail/', methods=['GET', 'POST'])
def detail(id):
    product = Product.query.get(id)
    return render_template('/product/detail.html', product=product)