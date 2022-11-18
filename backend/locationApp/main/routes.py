
from flask import Blueprint, render_template, request, abort, jsonify, current_app
from datetime import datetime
from locationApp import db
from locationApp.main.utils import filterPoints, getLocation
from locationApp.models import LocationPoint, ApiKey, Equipment
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import func
import requests
import random
import os

main = Blueprint('main', __name__)


@main.route("/")
def index():
  if current_user.is_authenticated:
    equipment = Equipment.query.filter(Equipment.user_id == current_user.id).all()
    return render_template('home.html', user_points=current_user.points, points_json=getLocation(), title='Your maps', equipment=equipment)
  else:
    f = open(os.path.join(current_app.config['CONTENT_DIR'], "Anonymous.md") , "r")
    mkd_content = f.read()
    return render_template("single.html", mkd_content=mkd_content, title='Home page')

@main.route("/about")
def about():
  f = open(os.path.join(current_app.config['CONTENT_DIR'], "About.md"), "r")
  mkd_content = f.read()
  return render_template("about.html", title='About project', mkd_content=mkd_content)

@main.route("/api/newpoint", methods=['POST', 'GET'])
def addPoint():
  key = ApiKey.query.filter_by(key=request.args.get('apikey')).first()
  if not key:
    abort(403)
  data = request.json
  location_point = LocationPoint(timestamp=datetime.now(),
      latitude=float(data['latitude']), longitude=float(data['longitude']), user_id=key.user_id, equipment=key.equipment)
  db.session.add(location_point)
  db.session.commit()
  return {'result': 'sucess'}

@main.route("/api/listpoints", methods=['POST', 'GET'])
@login_required
def listPoints():
  data = request.json
  return jsonify(filterPoints(data))

@main.route("/test", methods=['POST', 'GET'])
def test():
  latit = random.uniform(17, 22)
  longit = random.uniform(47.8, 49.1)
  api_key = ApiKey.query.filter(ApiKey.user_id==current_user.id, ApiKey.equipment is not None).order_by(func.random()).first()
  res = requests.post('http://localhost:8000/api/newpoint?apikey=' + api_key.key, json={"latitude":str(latit), "longitude":str(longit)})
  return 'success'