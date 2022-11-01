from datetime import datetime
from genericpath import exists
from locationApp.models import LocationPoint, Equipment
from flask_login import current_user

def filterPoints(criteria={}):
  points = {}
  date_to = datetime.max
  date_from = datetime.min
  if 'date_to' in criteria.keys():
    date_to = datetime.fromtimestamp(criteria['date_to']) 
  if 'date_from' in criteria.keys():
    date_from = datetime.fromtimestamp(criteria['date_from'])
  valid_points = LocationPoint.query.filter(LocationPoint.timestamp >= date_from, LocationPoint.timestamp <= date_to, LocationPoint.user_id == current_user.id)
  for point in valid_points:
    equip = Equipment.query.filter(Equipment.id == point.equipment).first()
    print(equip)
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