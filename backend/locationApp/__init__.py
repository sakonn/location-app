from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from locationApp.config import Config


#app.config['SECRET_KEY'] = '1bf5e2ce1bd28700fd2cfb4d013e8cc2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../db/site.db'
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  from locationApp.users.routes import users
  from locationApp.main.routes import main
  from locationApp.borrow.routes import borrow
  app.register_blueprint(users)
  app.register_blueprint(main)
  app.register_blueprint(borrow)

  return app
  