import json
import os
import time

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import jinja2
import webapp2

config = {
    'lat': 42.349939,
    'lng': -71.072653,
    'precip_threshold': 0.5,
    'cloud_threshold': 0.5
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),"templates")))

class ApiKey(ndb.Model):
    key = ndb.StringProperty()

def getForecast():
    api_key = ApiKey.get_by_id('key').key
    url = "https://api.forecast.io/forecast/%s/%s,%s" % (api_key,config['lat'],config['lng'])
    result = memcache.get('json')
    if result is not None:
        return result
    result = json.loads(urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=0'}).content)
    memcache.add(key='json',value=result,time=600)
    return result

def getBeaconClass():
    f = getForecast()['currently']
    if False:
        return "sox-champs"
    elif False:
        return "sox-rainout"
    elif f['precipProbability']>config['precip_threshold']:
        if f['precipType'] in ['rain','hail']:
            return 'rain'
        else:
            return 'snow'
    elif f['cloudCover']>config['cloud_threshold']:
        return 'clouds'
    else:
        return 'clear'

def getSunClass():
    f = getForecast()['daily']['data'][0]
    now = time.time()
    if now > f['sunriseTime'] and now < f['sunsetTime']:
        return 'day'
    else:
        return 'night'

def getClasses():
    """ Possible classes:
    beacon-clear
    beacon-clouds
    beacon-rain
    beacon-snow
    beacon-sox-rainout
    beacon-sox-champs

    sun-day
    sun-night
    """
    return ["beacon-"+getBeaconClass(),"sun-"+getSunClass()]

class MainPage(webapp2.RequestHandler):
    def get(self):
        classes = getClasses()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'classes':classes}))

class Script(webapp2.RequestHandler):
    def get(self):
        classes = getClasses()
        self.response.headers['Content-Type'] = 'application/javascript'
        template = JINJA_ENVIRONMENT.get_template('script.js')
        self.response.write(template.render({'classes':classes}))

class SetKey(webapp2.RequestHandler):
    def post(self):
        ApiKey.get_or_insert('key',key=self.request.get('key'))
        self.response.write("you did it")


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/script.js', Script),
    ('/set_key', SetKey),
    ], debug=True)
