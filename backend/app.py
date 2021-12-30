from locationApp.config import Config
from locationApp import create_app
import sqlalchemy_utils
from locationApp import db 

#if not sqlalchemy_utils.database_exists(Config.SQLALCHEMY_DATABASE_URI):
#  sqlalchemy_utils.create_database(Config.SQLALCHEMY_DATABASE_URI)

app = create_app()

if __name__ == '__main__':
  app.run(debug=True, port=5000)
