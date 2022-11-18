from datetime import datetime
from genericpath import exists
from locationApp.models import LocationPoint, Equipment
from flask_login import current_user


def filterPoints(criteria={}):
  points = {}
  date_to = datetime.max
  date_from = datetime.min
  if 'date_to' in criteria.keys() and criteria['date_to'] is not None:
    date_to = datetime.fromtimestamp(criteria['date_to']) 
  if 'date_from' in criteria.keys() and criteria['date_from'] is not None:
    date_from = datetime.fromtimestamp(criteria['date_from'])
  query = LocationPoint.query.filter(LocationPoint.timestamp >= date_from, LocationPoint.timestamp <= date_to, LocationPoint.user_id == current_user.id)
  if 'equipment' in criteria.keys() and len(criteria['equipment']) > 0:
    query = query.filter(LocationPoint.equipment.in_(criteria['equipment']))
  valid_points = query.all()
  for point in valid_points:
    equip = Equipment.query.filter(Equipment.id == point.equipment).first()
    points[str(point.id)] = {
      'lon': point.latitude,
      'lat': point.longitude,
      'timestamp': point.timestamp,
      'equipment': {
        'name': equip.name,
        'id': equip.id
      }
    }
  return points

def getLocation(criteria={}):
  points = {}
  valid_points = []
  for equip in Equipment.query.filter(Equipment.user_id == current_user.id, Equipment.locations != None):
    valid_points.append(LocationPoint.query.order_by(LocationPoint.id.desc()).filter(LocationPoint.equipment == equip.id).first())
  for point in valid_points:
    equip = Equipment.query.filter(Equipment.id == point.equipment).first()
    points[str(point.id)] = {
      'lon': point.latitude,
      'lat': point.longitude,
      'timestamp': point.timestamp,
      'equipment': {
        'name': equip.name,
        'id': equip.id
      }
    }
  return points