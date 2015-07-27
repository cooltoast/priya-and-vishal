from flask import Flask
from flask import render_template
app = Flask(__name__)

def render_page(name, *args, **kwargs):
    kwargs['selected'] = name
    return render_template('%s.html' % name, *args, **kwargs)

@app.route("/")
def home():
  return render_page('main')

@app.route("/itinerary")
def itinerary():
  return render_page('itinerary')

@app.route("/details")
def details():
  return render_page('details')

@app.route("/photos")
def photos():
  return render_page('photos')

@app.route("/photos/college-years")
def collegeYears():
  return render_page('college-years')

@app.route("/photos/engagement")
def engagement():
  return render_page('engagement')

@app.route("/registry")
def registry():
  return render_page('registry')

@app.route("/hello")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
