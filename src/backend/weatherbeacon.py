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

def isDev():
    return os.environ.get('SERVER_SOFTWARE','').startswith('Development')

def getForecast():
    result = memcache.get('json')
    if result is not None:
        return result
    key_obj = ApiKey.get_by_id('key')
    if isDev() and key_obj is None:
        url = "https://weather-beacon.appspot.com/forecast.json"
    else:
        api_key = key_obj.key
        url = "https://api.forecast.io/forecast/%s/%s,%s" % (api_key,config['lat'],config['lng'])
    result = json.loads(urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=0'}).content)
    memcache.add(key='json',value=result,time=600)
    return result

def describeConditions(f):
    if f['precipProbability']>config['precip_threshold']:
        if f['precipType'] in ['rain','hail']:
            return 'raining'
        else:
            return 'snowing'
    elif f['cloudCover']>config['cloud_threshold']:
        return 'cloudy'
    else:
        return 'clear'

def getBeaconClass():
    if False:
        return "sox-champs"
    elif False:
        return "sox-rainout"
    else:
        return describeConditions(getForecast()['currently'])

def getSunClass():
    f = getForecast()['daily']['data'][0]
    now = time.time()
    if now > f['sunriseTime'] and now < f['sunsetTime']:
        return 'daytime'
    else:
        return 'nighttime'

def getClasses():
    """ Possible classes:
    is-clear
    is-cloudy
    is-raining
    is-snowing
    is-sox-rainout
    is-sox-champs

    is-daytime
    is-nighttime
    """
    return ["is-"+getBeaconClass(),"is-"+getSunClass()]

class MainPage(webapp2.RequestHandler):
    def get(self):
        if isDev() and self.request.get('classes'):
            classes = self.request.get('classes').split(" ")
        else:
            classes = getClasses()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'classes':classes}))

class ForecastJson(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(getForecast()))

class SetKey(webapp2.RequestHandler):
    def post(self):
        ApiKey.get_or_insert('key',key=self.request.get('key'))
        self.redirect("/")


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/forecast.json', ForecastJson),
    ('/set_key', SetKey),
    ], debug=True)
