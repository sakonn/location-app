from flask import Blueprint, render_template, url_for, flash, redirect
from datetime import datetime
from locationApp import db
from locationApp.borrow.forms import BorrowForm
from locationApp.models import Borrow


borrow = Blueprint('borrow', __name__)



@borrow.route("/borrow-list", methods=['POST', 'GET'])
def borrow_list():
  borrows = Borrow.query.filter(Borrow.borrowed_to!= datetime.max).order_by(Borrow.id.desc())
  active = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
  return render_template('borrow_list.html', borrows=borrows, active=active)

@borrow.route("/borrow/new", methods=['POST', 'GET'])
def borrow_new():
  form = BorrowForm()
  if form.validate_on_submit():
    borrow = Borrow(client=form.client.data)
    db.session.add(borrow)
    db.session.commit()
    flash('Your borrow has been created, you are able to use it!', 'success')
    return redirect(url_for('borrow.borrow_list'))
  return render_template('borrow_new.html', form=form)

@borrow.route("/borrow/<int:borrow_id>", methods=['POST', 'GET'])
def borrow_view(borrow_id):
  borrow = Borrow.query.get_or_404(borrow_id)
  stoppable = borrow.borrowed_to >= datetime.utcnow()
  return render_template('borrow.html', borrow=borrow, stoppable=stoppable)

@borrow.route("/borrow/<int:borrow_id>/stop", methods=['POST', 'GET'])
def borrow_stop(borrow_id):
  borrow = Borrow.query.get_or_404(borrow_id)
  borrow.borrowed_to = datetime.utcnow()
  db.session.commit()
  flash('Your borrow has been stopped!', 'success')
  return redirect(url_for('main.index'))

@borrow.route("/borrow/<int:borrow_id>/delete", methods=['POST', 'GET'])
def borrow_delete(borrow_id):
  borrow = Borrow.query.get_or_404(borrow_id)
  db.session.delete(borrow)
  db.session.commit()
  flash('Your borrow has been deleted!', 'success')
  return redirect(url_for('borrow.borrow_list'))
