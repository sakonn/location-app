# usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.widgets.core import DateTimeLocalInput
from locationApp.models import User, ApiKey
from flask_login import current_user


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confimPassword = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken, please choose different one!')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken, please choose different one!')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])

  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember me')

  submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
      if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
          raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
      if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
          raise ValidationError('That email is taken. Please choose a different one.')

class KeyForm(FlaskForm):
  name = StringField('Key name', validators=[DataRequired()])
  key = StringField('Key', validators=[])
  
  submit = SubmitField('Save key')

class BorrowForm(FlaskForm):
  client = StringField('Klient name', validators=[DataRequired()])
  submit = SubmitField('Save borrow')

#  def validate_key(self, key):
#    user = ApiKey.query.filter_by(key=key.data).first()
#    if user:
#      raise ValidationError('Key already exist, generate new!')