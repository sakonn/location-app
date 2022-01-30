from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from datetime import datetime
from locationApp import db
from locationApp.models import Borrow
from locationApp.forms import KeyForm
from locationApp.models import LocationPoint, ApiKey, Borrow
from flask_login import current_user
from secrets import token_hex
import requests
import sqlalchemy_utils

main = Blueprint('main', __name__)


@main.route("/")
def index():
  active_borrow = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
  data = "" # To be filled probably
  return render_template('home.html', data=data, borrow=active_borrow)

@main.route("/about")
def about():
  return "<h1>Hello World about</h1>"

@main.route("/api/newpoint", methods=['POST', 'GET'])
def addPoint():
  if not ApiKey.query.filter_by(key=request.args.get('apikey')).first():
    abort(403)
  active_borrow = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
#  print(active_borrow)
  data = request.json
#  print(type(float(data['latitude'])))
#  print(data.latitude)
  location_point = LocationPoint(timestamp=datetime.now(), latitude=float(data['latitude']), longitude=float(data['longitude']), borrow=active_borrow)
  db.session.add(location_point)
  db.session.commit()
#  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#  latitude = db.Column(db.Float, nullable=False)
#  longitude = db.Column(db.Float, nullable=False)
#  borrow_id = db.Column(db.Integer, db.ForeignKey('borrow.id'), nullable=False) 
# print(content)
#  print(request.args.get('apikey'))
  return {'pointID': location_point.id}

@main.route("/test", methods=['POST', 'GET'])
def test():
  res = requests.post('http://python-location.azurewebsites.net/api/newpoint?apikey=94f4495175fd40ce07148985bf86a498', json={"latitude":"12.34", "longitude": "56.78"})
  if res.ok:
    print(res.json())
  return 'success'