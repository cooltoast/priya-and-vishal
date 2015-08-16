import json
from flask import Flask, render_template, request
from twilio import twiml

app = Flask(__name__)

try:
  AUTHORIZED_SENDERS = json.load(open("authorized_senders.json"))
except Exception as e:
  print(e)
  print("NO SENDERS AUTHORIZED")
  AUTHORIZED_SENDERS = []


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

@app.route("/photos")
def photos():
  return render_page('photos')

@app.route("/twilio", methods=['GET', 'POST'])
def twilio():
  resp = twiml.Response()
  sender = request.values.get('From', None)
  body = request.values.get('Body', None)

  if sender in AUTHORIZED_SENDERS:
    if body is not None:
      print("%s: %s" % (sender, body))
      resp.message("test")
    else:
        resp.message("but no message")
  else:
    resp.message("no youre not authorized")

  return str(resp)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
