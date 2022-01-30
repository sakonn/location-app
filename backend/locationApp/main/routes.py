from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from datetime import datetime
from locationApp import db
from locationApp.forms import KeyForm
from locationApp.models import LocationPoint, ApiKey, User
from flask_login import current_user
from secrets import token_hex
import requests

main = Blueprint('main', __name__)


@main.route("/")
def index():
#  db.create_all()
#  active_borrow = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
  if current_user.is_authenticated:
    points = {}
    for point in current_user.points:
      points[str(point.id)] = {
        'lon': point.latitude,
        'lat': point.longitude,
        'timestamp': point.timestamp
      }
    return render_template('home.html', user_points=current_user.points, points_json=points)
  else:
    return render_template("home_anonymous.html")

@main.route("/about")
def about():
  return "<h1>Hello World about</h1>"

@main.route("/api/newpoint", methods=['POST', 'GET'])
def addPoint():
  key = ApiKey.query.filter_by(key=request.args.get('apikey')).first()
  if not key:
    abort(403)
  data = request.json
  location_point = LocationPoint(timestamp=datetime.now(), latitude=float(data['latitude']), longitude=float(data['longitude']), user_id=key.user_id)
  db.session.add(location_point)
  db.session.commit()
  return {'result': 'sucess'}

@main.route("/test", methods=['POST', 'GET'])
def test():
  res = requests.post('http://127.0.0.1:5000/api/newpoint?apikey=b2a2081e32bf96957180e74d7cce1976', json={"latitude":"12.84", "longitude": "52.78"})
  if res.ok:
    print(res.json())
  return 'success'