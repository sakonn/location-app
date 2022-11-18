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
  form = EquipForm()
  if form.validate_on_submit():
    equip = Equipment(name=form.name.data, description=form.description.data, owner=current_user)
    if form.image.data:
      picture_files = save_picture(form.image.data)
      equip.image_small = picture_files[0]
      equip.image_medium = picture_files[1]
      equip.image_large = picture_files[2]
    db.session.add(equip)
    db.session.commit()
    flash('Your equipment has been created!', 'success')
    return redirect(url_for('equip.equip_list'))
  # image_file = url_for('static', filename="equip_pics/" + )
  return render_template('equip_form.html', form=form, title='Hello ' + current_user.username, form_title="Add equipment")

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

@equip.route("/equipment/<int:equip_id>/edit", methods=['POST', 'GET'])
@login_required
def equip_edit(equip_id):
  form = EquipForm()
  equip:Equipment = Equipment.query.get_or_404(equip_id)
  if form.validate_on_submit():
    equip.name = form.name.data
    equip.description = form.description.data
    if form.image.data:
      picture_files = save_picture(form.image.data)
      equip.image_small = picture_files[0]
      equip.image_medium = picture_files[1]
      equip.image_large = picture_files[2]
    db.session.commit()
    flash('Your key has been updated, you are able to use it!', 'success')
    return redirect(url_for('equip.equip_list'))
  elif request.method == 'GET':
    form.name.data = equip.name
    form.description.data = equip.description
    form.image.data = equip.image_medium
  return render_template('equip_form.html', form=form, title='Hello ' + current_user.username, form_title="Update equipment")
