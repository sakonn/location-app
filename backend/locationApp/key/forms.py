from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from locationApp.models import Equipment
from flask_login import current_user

class KeyForm(FlaskForm):
  name = StringField('Key name', validators=[DataRequired()])
  key = StringField('Key', validators=[])
  equipment = SelectField('Equipment', choices=[], coerce=int, validate_choice=False, validators=[DataRequired()])

  submit = SubmitField('Save key')

#  def validate_key(self, key):
#    user = ApiKey.query.filter_by(key=key.data).first()
#    if user:
#      raise ValidationError('Key already exist, generate new!')