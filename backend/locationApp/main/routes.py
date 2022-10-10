
from flask import Blueprint, render_template, request, abort, jsonify, current_app
from datetime import datetime
from locationApp import db
from locationApp.main.utils import filterPoints
from locationApp.models import LocationPoint, ApiKey
from flask_login import current_user, login_required
import requests
import random

main = Blueprint('main', __name__)


@main.route("/")
def index():
#  db.create_all()
#  active_borrow = Borrow.query.filter(Borrow.borrowed_to >= datetime.utcnow()).first()
  if current_user.is_authenticated:
    return render_template('home.html', user_points=current_user.points, points_json=filterPoints(), title='Your maps')
  else:
    f = open(current_app.config['CONTENT_DIR'] + "\Anonymous.md", "r")
    mkd_content = f.read()
    return render_template("single.html", mkd_content=mkd_content, title='Home page')

@main.route("/about")
def about():
  f = open(current_app.config['CONTENT_DIR'] + "\About.md", "r")
  mkd_content = f.read()
  return render_template("single.html", title='About project', mkd_content=mkd_content)

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

@main.route("/api/listpoints", methods=['POST', 'GET'])
@login_required
def listPoints():
  data = request.json
  print(data)
  return jsonify(filterPoints(data))

@main.route("/test", methods=['POST', 'GET'])
def test():
  latit = random.uniform(17, 22)
  longit = random.uniform(47.8, 49.1)
  res = requests.post('http://localhost:5000/api/newpoint?apikey=8a14eb966504b7c2dc4b220f4f5be970', json={"latitude":str(latit), "longitude":str(longit)})
  if res.ok:
    print(res.json())
  return 'success'