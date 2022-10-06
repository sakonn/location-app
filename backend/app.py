from locationApp import create_app

#if not sqlalchemy_utils.database_exists('sqlite:///../db/site.db'):
#  sqlalchemy_utils.create_database('sqlite:///../db/site.db')

app = create_app()

if __name__ == '__main__':
  app.run(debug=True, port=5000)
  # app.run(host='0.0.0.0', port=5000)
