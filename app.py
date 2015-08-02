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

@app.route("/attractions")
def attractions():
  return render_page('attractions')

@app.route("/newsfeed")
def newsfeed():
  return render_page('newsfeed')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
