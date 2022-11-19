from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class EquipForm(FlaskForm):
  name = StringField('Equipment name', validators=[DataRequired()])
  description = TextAreaField('Description', validators=[])
  image = FileField('Upload image', validators=[FileAllowed(['jpg', 'png'])])
  
  submit = SubmitField('Save equipment')

class NewEquipForm(FlaskForm):
  name = StringField('Equipment name', validators=[DataRequired()])
  description = TextAreaField('Description', validators=[])
  image = FileField('Upload image', validators=[FileAllowed(['jpg', 'png'])])
  
  submit = SubmitField('Create equipment')