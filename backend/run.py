from locationApp import create_app
import sqlalchemy_utils

if not sqlalchemy_utils.database_exists('sqlite:///site.db'):
  sqlalchemy_utils.create_database('sqlite:///site.db')

app = create_app()

if __name__ == '__main__':
  app.run(debug=True, port=5000)
