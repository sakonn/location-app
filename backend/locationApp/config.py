import os
from dotenv import load_dotenv
import urllib.parse 

load_dotenv()

class Config:
  params = urllib.parse.quote_plus(os.environ.get('SQLALCHEMY_DATABASE_URI'))

  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
#  SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_COMMIT_ON_TEARDOWN = True