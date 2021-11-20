from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = '1bf5e2ce1bd28700fd2cfb4d013e8cc2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/site.db'
db = SQLAlchemy(app)

from locationApp import routes