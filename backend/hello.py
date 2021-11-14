# import os
# from flask import Flask
# import mysql.connector


# class DBManager:
#     def __init__(self, database='example', host="db", user="root", password_file=None):
#         pf = open(password_file, 'r')
#         self.connection = mysql.connector.connect(
#             user=user, 
#             password=pf.read(),
#             host=host, # name of the mysql service as set in the docker-compose file
#             database=database,
#             auth_plugin='mysql_native_password'
#         )
#         pf.close()
#         self.cursor = self.connection.cursor()
    
#     def populate_db(self):
#         self.cursor.execute('DROP TABLE IF EXISTS blog')
#         self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
#         self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,7)])
#         self.connection.commit()
    
#     def query_titles(self):
#         self.cursor.execute('SELECT title FROM blog')
#         rec = []
#         for c in self.cursor:
#             rec.append(c[0])
#         return rec


# server = Flask(__name__)
# conn = None

# @server.route('/')
# def listBlog():
#     global conn
#     if not conn:
#         conn = DBManager(password_file='/run/secrets/db-password')
#         conn.populate_db()
#     rec = conn.query_titles()

#     response = ''
#     for c in rec:
#         response = response  + '<div>   Hello  ' + c + '</div></br>'
#     return response


# if __name__ == '__main__':
#     server.run(debug=True)

from flask import Flask, render_template
app = Flask(__name__)


data = [
   {
      'author': 'Author 1',
      'title': 'Title 1',
      'content': 'Content 1'
   },
   {
      'author': 'Author 2',
      'title': 'Title 2',
      'content': 'Content 2'
   },
   {
      'author': 'Author 3',
      'title': 'Title 3',
      'content': 'Content 3'
   }
]



@app.route("/")
def index():
   return render_template('home.html', data=data)

@app.route("/about")
def about():
   return "<h1>Hello World about</h1>"

if __name__ == '__main__':
  app.run(debug=True, port=80)