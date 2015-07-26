from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def home():
  return render_template('main.html')

@app.route("/details")
def details():
  return render_template('details.html')

@app.route("/photos")
def photos():
  return render_template('photos.html')

@app.route("/photos/college-years")
def collegeYears():
  return render_template('college-years.html')

@app.route("/photos/engagement")
def engagement():
  return render_template('engagement.html')

@app.route("/registry")
def registry():
  return render_template('registry.html')

@app.route("/hello")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()
