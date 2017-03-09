from flask.ext.sqlalchemy import SQLAlchemy ##import sqlalchemy
from werkzeug import generate_password_hash, check_password_hash##store password
##into hash so that won`t allow user password hacked
from werkzeug.utils import secure_filename
import geocoder## use wikigeodataapi to find place that arount perticular places
##and store in xml file in wikimedia servers.This class will wrap the api into app
import urllib2
import json

db = SQLAlchemy()## variable named db contain instance of SQLAlchemy class

class User(db.Model):## CLASS use to model the uses`s table.This should have
##same attribute as the table that create in postgres database
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
## constructor that use to store firstname/lastname/email/password
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname  ##.title()will capatal first letter
    self.lastname = lastname
    self.email = email ## .lower()will save to all lowercase
    self.hash_password(password) ## save the decode password

  def hash_password(self, password):  ## class use to decode password
    self.pwdhash = generate_password_hash(password) ## method that from werkzeug library
    ## use to security passwod

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)



##model that wrap the geocoder api

class Place(object):
  def meters_to_walking_time(self, meters):
    return int(meters / 100)## 100 meters walk/min

  def wiki_path(self, slug):
    return urllib2.urlparse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

  def address_to_latlng(self, address):
    g = geocoder.google(address)
    return (g.lat, g.lng)

  def query(self, address):
    lat, lng = self.address_to_latlng(address)

    query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
    g = urllib2.urlopen(query_url)
    results = g.read()
    g.close()

    data = json.loads(results)

    places = []
    for place in data['query']['geosearch']:
      name = place['title']
      meters = place['dist']
      lat = place['lat']
      lng = place['lon']

      wiki_url = self.wiki_path(name)
      walking_time = self.meters_to_walking_time(meters)

      d = {
        'name': name,
        'url': wiki_url,
        'time': walking_time,
        'lat': lat,
        'lng': lng
      }

      places.append(d)

    return places
