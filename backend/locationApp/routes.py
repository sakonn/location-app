from flask import render_template, url_for, flash, redirect
from locationApp import app
from locationApp.forms import RegistrationForm, LoginForm
from locationApp.models import Users, LocationPoint

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
  form = RegistrationForm()
  if form.validate_on_submit():
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('index'))
  return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@blog.com' and form.password.data == 'password':
      flash(f'You have been loggen in!', 'success')
      return redirect(url_for('index'))
    else:
        flash(f'Login unsuccessfull !', 'danger')
  return render_template('login.html', title='Log in', form=form)
