from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])

  email = StringField('Email', validators=[DataRequired(), Email()])

  password = PasswordField('Password', validators=[DataRequired()])
  confimPassword = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

  submit = SubmitField('Register')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])

  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember me')

  submit = SubmitField('Log in')