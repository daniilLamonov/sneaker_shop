from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user

from ..forms import RegistrationForm, LoginForm
from ..models.user import User
from ..extensions import db, bcrypt

user = Blueprint('user', __name__)

@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to login', 'success')
            return redirect(url_for('user.login'))
        except Exception as e:
            print(e)
            flash('There was an error creating your account', 'danger')
    return render_template('user/register.html', form=form)


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You are now logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login failed.', 'danger')
    return render_template('user/login.html', form=form)



@user.route('/user/logout')
def logout():
     logout_user()
     return redirect(url_for('main.index'))
