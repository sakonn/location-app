
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from locationApp.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)], render_kw={'x-model': 'username'})
  email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'x-model': 'email'})
  password = PasswordField('Password', validators=[DataRequired()], render_kw={'x-model': 'password'})
  confimPassword = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')], render_kw={'x-model': 'passConfirm'})

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

class RequestResetForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is None:
      raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Reset Password')