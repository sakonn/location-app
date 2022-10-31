from fileinput import filename
from unicodedata import name
from flask import Blueprint, render_template, url_for, flash, redirect, request
from locationApp import db
from flask_login import current_user, login_required
from locationApp.equip.forms import EquipForm, NewEquipForm
from locationApp.equip.utils import save_picture
from locationApp.models import Equipment
from secrets import token_hex
equip = Blueprint('equip', __name__)

@equip.route("/equipment/list", methods=['GET'])
@login_required
def equip_list():
  equipment = Equipment.query.filter(Equipment.user_id == current_user.id).all()
  return render_template('equip_list.html', equipment=equipment, title='Hello ' + current_user.username)

@equip.route("/equipment/new", methods=['POST', 'GET'])
@login_required
def equip_new():
  form = NewEquipForm()
  if form.validate_on_submit():
    equip = Equipment(name=form.name.data, description=form.description.data, owner=current_user)
    print(form.image)
    if form.image.data:
      picture_file = save_picture(form.image.data)
      equip.image_file = picture_file
    db.session.add(equip)
    db.session.commit()
    flash('Your equipment has been created!', 'success')
    return redirect(url_for('equip.equip_list'))
  # image_file = url_for('static', filename="equip_pics/" + )
  return render_template('equip_form.html', form=form, title='Hello ' + current_user.username)

@equip.route("/equipment/<int:equip_id>/delete", methods=['POST', 'GET'])
@login_required
def equip_delete(equip_id):
  equip = Equipment.query.get_or_404(equip_id)
  if equip.owner.id == current_user.id:
    db.session.delete(equip)
    db.session.commit()
    flash('Your equipment has been deleted!', 'success')
  else:
    flash('Sorry but you are not authorized to modify this equipment', 'error')
  return redirect(url_for('equip.equip_list'))

# @key.route("/key/<int:key_id>/delete", methods=['POST', 'GET'])
# @login_required
# def key_delete(key_id):
#   key = ApiKey.query.get_or_404(key_id)
#   if key.owner.id == current_user.id:
#     db.session.delete(key)
#     db.session.commit()
#     flash('Your key has been deleted!', 'success')
#   else:
#     flash('Sorry but you are not authorized to modify this key', 'error')
#   return redirect(url_for('key.key_list'))


# @key.route("/key/<int:key_id>/edit", methods=['POST', 'GET'])
# @login_required
# def key_edit(key_id):
#   form = KeyForm()
#   key = ApiKey.query.get_or_404(key_id)
#   if form.validate_on_submit():
#     key.name = form.name.data
#     db.session.commit()
#     flash('Your key has been updated, you are able to use it!', 'success')
#     return redirect(url_for('key.key_list'))
#   elif request.method == 'GET':
#     form.key.data = key.key
#     form.name.data = key.name
#   return render_template('key_form.html', form=form, title='Hello ' + current_user.username, form_title="Update key")
