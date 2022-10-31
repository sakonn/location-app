from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class EquipForm(FlaskForm):
  name = StringField('Equipment name', validators=[DataRequired()])
  
  submit = SubmitField('Save key')

#  def validate_key(self, key):
#    user = ApiKey.query.filter_by(key=key.data).first()
#    if user:
#      raise ValidationError('Key already exist, generate new!')

class NewEquipForm(FlaskForm):
  name = StringField('Equipment name', validators=[DataRequired()])
  description = TextAreaField('Description', validators=[])
  image = FileField('Upload image', validators=[FileAllowed(['jpg', 'png'])])
  
  submit = SubmitField('Create equipment')