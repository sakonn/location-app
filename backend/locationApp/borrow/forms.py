from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BorrowForm(FlaskForm):
  client = StringField('Klient name', validators=[DataRequired()])
  submit = SubmitField('Save borrow')
