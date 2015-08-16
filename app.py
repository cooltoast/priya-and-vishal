import json
from flask import Flask, render_template, request, g
from twilio import twiml
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.db')

try:
  AUTHORIZED_SENDERS = json.load(open("authorized_senders.json"))
except Exception as e:
  print(e)
  print("NO SENDERS AUTHORIZED")
  AUTHORIZED_SENDERS = []

def init_db():
  with app.app_context():
    db = get_db()
    db.cursor().executescript("""
      CREATE table IF NOT EXISTS newsfeed (sender TEXT, timestamp TEXT, message TEXT)
    """)
    db.commit()

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
  db.row_factory = sqlite3.Row
  return db

def insert_db(query, args=()):
  cur = get_db().execute(query, args)
  cur.close()

def query_db(query, args=(), one=False):
  cur = get_db().execute(query, args)
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

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
  news = query_db("select * from newsfeed")
  return render_page('newsfeed', news=news)

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
      insert_db('insert into newsfeed values(?,?,?)', (sender, str(datetime.datetime.now()), body))
      resp.message("test")
    else:
        resp.message("but no message")
  else:
    resp.message("no youre not authorized")

  return str(resp)

if __name__ == "__main__":
  init_db()
  app.run(host='0.0.0.0', debug=True)
