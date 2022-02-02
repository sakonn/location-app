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
  MAIL_SERVER = 'mail.korecko.eu'
  MAIL_PORT = 465
  MAIL_USE_TLS = False
  MAIL_USE_SSL = True
  MAIL_DEBUG = False
  MAIL_SUPPRESS_SEND = False
  MAIL_DEFAULT_SENDER = os.environ.get('DEFAULT_SENDER')
  MAIL_USERNAME = os.environ.get('EMAIL_USER')
  MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
  CONTENT_DIR = os.environ.get('CONTENT_DIR')