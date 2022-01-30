from flask import Blueprint, render_template, url_for, flash, redirect, request
from locationApp import db
from flask_login import current_user
from locationApp.key.forms import KeyForm
from locationApp.models import ApiKey
from secrets import token_hex
import requests


key = Blueprint('key', __name__)

@key.route("/key-list", methods=['POST', 'GET'])
def key_list():
#  key = ApiKey.query.filter_by(owner=current_user)
  keys = ApiKey.query.all()
#  active = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
  return render_template('key_list.html', keys=keys)

@key.route("/key/new", methods=['POST', 'GET'])
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
  return render_template('key_new.html', form=form)

@key.route("/key/<int:key_id>/delete", methods=['POST', 'GET'])
def key_delete(key_id):
  key = ApiKey.query.get_or_404(key_id)
  db.session.delete(key)
  db.session.commit()
  flash('Your key has been deleted!', 'success')
  return redirect(url_for('key.key_list'))
