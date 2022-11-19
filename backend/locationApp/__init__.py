from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from locationApp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_misaka import Misaka
from flask_assets import Environment, Bundle
from locationApp.assets import bundles

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'
mail = Mail()
misaka = Misaka()
assets = Environment()
csrf = CSRFProtect()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  from locationApp.users.routes import users
  from locationApp.main.routes import main
  from locationApp.key.routes import key
  from locationApp.equip.routes import equip
  app.register_blueprint(users)
  app.register_blueprint(main)
  app.register_blueprint(key)
  app.register_blueprint(equip)

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)
  misaka.init_app(app)
  csrf.init_app(app)
  assets.init_app(app)
  assets.register(bundles)

  return app
  