from flask import Blueprint, render_template, url_for, flash, redirect, request
from locationApp import db
from flask_login import current_user, login_required
from locationApp.key.forms import KeyForm
from locationApp.models import ApiKey
from secrets import token_hex


key = Blueprint('key', __name__)

@key.route("/key-list", methods=['POST', 'GET'])
@login_required
def key_list():
  keys = ApiKey.query.filter(ApiKey.user_id == current_user.id).all()
  return render_template('key_list.html', keys=keys, title='Hello ' + current_user.username)

@key.route("/key/new", methods=['POST', 'GET'])
@login_required
def key_new():
  form = KeyForm()
  if form.validate_on_submit():
    key = ApiKey(name=form.name.data, key=form.key.data, owner=current_user)
    db.session.add(key)
    db.session.commit()
    flash('Your key has been created, you are able to use it!', 'success')
    return redirect(url_for('key.key_list'))
  elif request.method == 'GET':
    form.key.data = token_hex(nbytes=16)
  return render_template('key_new.html', form=form, title='Hello ' + current_user.username)

@key.route("/key/<int:key_id>/delete", methods=['POST', 'GET'])
@login_required
def key_delete(key_id):
  key = ApiKey.query.get_or_404(key_id)
  if key.owner == current_user.id:
    db.session.delete(key)
    db.session.commit()
    flash('Your key has been deleted!', 'success')
  else:
    flash('Sorry but you are not authorized to modify this key', 'error')
  return redirect(url_for('key.key_list'))
