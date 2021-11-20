from flask import render_template, url_for, flash, redirect, request
from locationApp import app, db, bcrypt
from locationApp.forms import RegistrationForm, LoginForm, KeyForm
from locationApp.models import User, LocationPoint
from flask_login import login_user, current_user, logout_user, login_required
import secrets

data = [
  {
    'author': 'Author 1',
    'title': 'Title 1',
    'content': 'Content 1'
  },
  {
    'author': 'Author 2',
    'title': 'Title 2',
    'content': 'Content 2'
  },
  {
    'author': 'Author 3',
    'title': 'Title 3',
    'content': 'Content 3'
  }
]


@app.route("/")
def index():
  return render_template('home.html', data=data)

@app.route("/about")
def about():
  return "<h1>Hello World about</h1>"

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created, you are able to log in!', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      if next_page:
        return redirect(next_page)
      return redirect(url_for('index'))
    else:
      flash(f'Login unsuccessfull !', 'danger')
  return render_template('login.html', title='Log in', form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = KeyForm()
  return render_template('account.html', data=data, form=form, key=secrets.token_urlsafe(32))