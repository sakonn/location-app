from datetime import datetime
from locationApp import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_ser(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=True)
  keys = db.relationship('ApiKey', backref='owner', lazy=True)
  points = db.relationship('LocationPoint', backref='owner', lazy=True)
  equipment = db.relationship('Equipment', backref='owner', lazy=True)

  def get_reset_token(self, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': self.id}).decode('utf-8')
  
  @staticmethod
  def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return User.query.get(user_id)

  def __repr__(self):
    return f"User ('{self.username}', '{self.email}')"

class ApiKey(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  key = db.Column(db.String(32), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  equipment = db.Column(db.Integer, db.ForeignKey('equipment.id'))
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __repr__(self):
    return f"Key ('{self.name}')"

class LocationPoint(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  latitude = db.Column(db.Float, nullable=False)
  longitude = db.Column(db.Float, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  equipment = db.Column(db.Integer, db.ForeignKey('equipment.id'))

  def __repr__(self):
    return f"Point ('{self.id}', '{self.timestamp}')"

class Equipment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='000demo_equip.jpg')
  description = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  api_key = db.relationship('ApiKey', backref='equipment_key', lazy=True)
  locations = db.relationship('LocationPoint', backref='locations', lazy=True)

  def __repr__(self):
    return f"Equipement ('{self.name}')"


# class Borrow(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   client = db.Column(db.String(120), nullable=False)
#   borrowed_from = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#   borrowed_to = db.Column(db.DateTime, nullable=True, default=datetime.strptime('1/1/3000 0:0:0', '%m/%d/%Y %H:%M:%S'))
#   points = db.relationship('LocationPoint', backref='borrow', lazy=True)

#   def __repr__(self):
#     return f"Borrow ('{self.client}', '{self.borrowed_to}')"