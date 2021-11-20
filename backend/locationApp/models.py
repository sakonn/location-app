from datetime import datetime
from locationApp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_ser(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=True)
  keys = db.relationship('ApiKey', backref='owner', lazy=True)

  def __repr__(self):
    return f"User ('{self.username}', '{self.email}')"

class ApiKey(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  key = db.Column(db.String(32), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f"Key ('{self.name}')"

class LocationPoint(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  latitude = db.Column(db.Float, nullable=False)
  longitude = db.Column(db.Float, nullable=False)
  borrow_id = db.Column(db.Integer, db.ForeignKey('borrow.id'), nullable=False)

  def __repr__(self):
    return f"Point ('{self.id}', '{self.timestamp}')"

class Borrow(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  client = db.Column(db.String(120), nullable=False)
  borrowed_from = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  borrowed_to = db.Column(db.DateTime, nullable=True, default=datetime.min)
  points = db.relationship('LocationPoint', backref='borrow', lazy=True)

  def __repr__(self):
    return f"Borrow ('{self.client}', '{self.borrowed_to}')"