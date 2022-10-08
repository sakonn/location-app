from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from locationApp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_misaka import Misaka

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'
mail = Mail()
misaka = Misaka()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  from locationApp.users.routes import users
  from locationApp.main.routes import main
  from locationApp.key.routes import key
  app.register_blueprint(users)
  app.register_blueprint(main)
  app.register_blueprint(key)

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)
  misaka.init_app(app)

  return app
  