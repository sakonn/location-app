from locationApp import app
import sqlalchemy_utils

if not sqlalchemy_utils.database_exists('sqlite:///site.db'):
  sqlalchemy_utils.create_database('sqlite:///site.db')
  
if __name__ == '__main__':
#app.run(debug=True, port=5000)
  app.run(host="0.0.0.0")
