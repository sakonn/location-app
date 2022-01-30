from flask import Blueprint, render_template, url_for, flash, redirect, request
from locationApp import db, bcrypt
from locationApp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from locationApp.models import User, ApiKey
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created, you are able to log in!', 'success')
    return redirect(url_for('users.login'))
  return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      if next_page:
        return redirect(next_page)
      return redirect(url_for('main.index'))
    else:
      flash(f'Login unsuccessfull !', 'danger')
  return render_template('login.html', title='Log in', form=form)

@users.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  keys = ApiKey.query.filter_by(owner=current_user).all()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('users.account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  return render_template('account.html', keys=keys, form=form)
