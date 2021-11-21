from flask import render_template, url_for, flash, redirect, request
from datetime import datetime, date
from flask.templating import render_template_string
from locationApp import app, db, bcrypt
from locationApp.forms import RegistrationForm, LoginForm, KeyForm, BorrowForm, UpdateAccountForm
from locationApp.models import User, LocationPoint, ApiKey, Borrow
from flask_login import login_user, current_user, logout_user, login_required
import requests

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
  borrow = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
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
  form = UpdateAccountForm()
  keys = ApiKey.query.filter_by(owner=current_user).all()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  return render_template('account.html', keys=keys, form=form)

@app.route("/borrow-list", methods=['POST', 'GET'])
def borrow_list():
  borrows = Borrow.query.filter(Borrow.borrowed_to!= datetime.max).order_by(Borrow.id.desc())
  active = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
  return render_template('borrow_list.html', borrows=borrows, active=active)

@app.route("/borrow/new", methods=['POST', 'GET'])
def borrow_new():
  form = BorrowForm()
  if form.validate_on_submit():
    borrow = Borrow(client=form.client.data)
    db.session.add(borrow)
    db.session.commit()
    flash('Your borrow has been created, you are able to use it!', 'success')
    return redirect(url_for('borrow_list'))
  return render_template('borrow_new.html', form=form)

@app.route("/borrow/<int:borrow_id>", methods=['POST', 'GET'])
def borrow_view(borrow_id):
  borrow = Borrow.query.get_or_404(borrow_id)
  stoppable = borrow.borrowed_to >= datetime.utcnow()
  return render_template('borrow.html', borrow=borrow, stoppable=stoppable)

@app.route("/borrow/<int:borrow_id>/stop", methods=['POST', 'GET'])
def borrow_stop(borrow_id):
  borrow = Borrow.query.get_or_404(borrow_id)
  borrow.borrowed_to = datetime.utcnow()
  db.session.commit()
  flash('Your borrow has been stopped!', 'success')
  return redirect(url_for('index'))

@app.route("/borrow/<int:borrow_id>/delete", methods=['POST', 'GET'])
def borrow_delete(borrow_id):
  borrow = Borrow.query.get_or_404(borrow_id)
  db.session.delete(borrow)
  db.session.commit()
  flash('Your borrow has been deleted!', 'success')
  return redirect(url_for('borrow_list'))

@app.route("/api/newpoint", methods=['POST', 'GET'])
def addPoint():
  active_borrow = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
  content = request.json
  print(content)
  print(request.args.get('apikey'))
  return {'staus': 'ok'}


@app.route("/test", methods=['POST', 'GET'])
def test():
  res = requests.post('http://localhost:5000/api/newpoint?apikey=mykey', json={"mytext":"lalala"})
  if res.ok:
    print(res.json())
  return 'success'