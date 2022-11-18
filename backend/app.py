from locationApp import create_app
from locationApp import db

app = create_app()

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True, port=8000)
  # app.run(host='0.0.0.0', port=5000)
