from datetime import datetime
from locationApp import db

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=True)

  def __repr__(self):
    return f"User ('{self.username}', '{self.email}')"

class LocationPoint(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  latitude = db.Column(db.Float, nullable=False)
  longitude = db.Column(db.Float, nullable=False)
  borrow = db.relationship('Borrow', backref='points', lazy=True)

  def __repr__(self):
    return f"Point ('{self.id}', '{self.timestamp}')"

class Borrow(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  client = db.Column(db.String(120), nullable=False)
  borrowed_from = db.Column(db.DateTime, nullable=False)
  borrowed_to = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f"Borrow ('{self.client}', '{self.borrowed_to}')"