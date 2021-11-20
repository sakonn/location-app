from flask import render_template, url_for, flash, redirect, request
from locationApp import app, db, bcrypt
from locationApp.forms import RegistrationForm, LoginForm, KeyForm, BorrowForm
from locationApp.models import User, LocationPoint, ApiKey, Borrow
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
  borrow = Borrow.query.first()
  return render_template('home.html', data=data, borrow=borrow)

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
  borrrow_form = BorrowForm()
  keys = ApiKey.query.filter_by(owner=current_user).all()
  borrows = Borrow.query.all()
  if form.identifier.data == 'key_form' and form.validate_on_submit():
    key = ApiKey(name=form.name.data, key=form.key.data, owner=current_user)
    db.session.add(key)
    db.session.commit()
    flash('Your key has been created, you are able to use it!', 'success')
  elif borrrow_form.identifier.data == 'borrrow_form' and borrrow_form.validate_on_submit():
    borrow = Borrow(client=borrrow_form.client.data)
    db.session.add(borrow)
    db.session.commit()
    flash('Your borrow has been created, you are able to use it!', 'success')
  elif request.method == 'GET':
    form.key.data = secrets.token_urlsafe(32)
  return render_template('account.html', keys=keys, form=form, borrows=borrows, borrrow_form=borrrow_form)

@app.route("/api/newpoint", methods=['POST'])
def addPoint():
  borrow = ''
  return {'staus': 'ok'}