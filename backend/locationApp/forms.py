# usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.widgets.core import DateTimeLocalInput
from locationApp.models import User, ApiKey


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

class KeyForm(FlaskForm):
  identifier = StringField()
  name = StringField('Key name', validators=[DataRequired()])
  key = StringField('Key', validators=[DataRequired()])
  
  submit = SubmitField('Save key')

class BorrowForm(FlaskForm):
  identifier = StringField()
  client = StringField('Klient name', validators=[DataRequired()])
  
  submit = SubmitField('Save borrow')

#  def validate_key(self, key):
#    user = ApiKey.query.filter_by(key=key.data).first()
#    if user:
#      raise ValidationError('Key already exist, generate new!')