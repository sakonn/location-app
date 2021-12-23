# usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class KeyForm(FlaskForm):
  name = StringField('Key name', validators=[DataRequired()])
  key = StringField('Key', validators=[])
  
  submit = SubmitField('Save key')

#  def validate_key(self, key):
#    user = ApiKey.query.filter_by(key=key.data).first()
#    if user:
#      raise ValidationError('Key already exist, generate new!')