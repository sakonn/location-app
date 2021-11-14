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
  app.run(debug=True, port=1313)