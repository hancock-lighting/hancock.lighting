import json
import re
import os
import time

from google.appengine.api import memcache
from google.appengine.api import urlfetch

import jinja2
import webapp2
import yaml

def rel(path):
    return os.path.join(os.path.dirname(__file__),path)

try:
    with open(rel("secrets.yaml")) as fh:
        config = yaml.load(fh)
except Exception as e:
    print e
    config = {}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(rel("templates")))

def isDev():
    # return False
    return os.environ.get('SERVER_SOFTWARE','').startswith('Development')

def getForecast():
    result = memcache.get('forecast')
    if result is not None:
        return result
    url = "https://api.forecast.io/forecast/%s/%s,%s" % (config['forecast_io']['api_key'],config['weather']['lat'],config['weather']['lon'])
    result = json.loads(urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=0'}).content)
    memcache.add(key='forecast',value=result,time=120)
    return result

def describeConditions(f):
    if f['precipProbability']>config['weather']['precip_threshold']:
        if f['precipType'] in ['rain','hail']:
            return 'raining'
        else:
            return 'snowing'
    elif f['cloudCover']>config['weather']['cloud_threshold']:
        return 'cloudy'
    else:
        return 'clear'

def getSoxStatus():
    if False:
        return "sox-champs"
    elif False:
        return "sox-rainout"

def getSunClass(f):
    now = time.time()
    if now > f['sunriseTime'] and now < f['sunsetTime']:
        return 'daytime'
    else:
        return 'nighttime'

def buildStatus():
    f = getForecast()
    weather = describeConditions(f['currently'])
    return {
            'beacon': getSoxStatus() or weather,
            'weather': weather,
            'time': getSunClass(f['daily']['data'][0])
            }

def getStatus():
    if isDev():
        try:
            return json.loads(urlfetch.fetch("https://weather-beacon.appspot.com/v0/status.json", headers = {'Cache-Control' : 'max-age=0'}).content)
        except:
            return {'beacon': "clear", 'weather': "clear", 'time': "daytime"}
    result = memcache.get('status')
    if result is not None:
        return result
    result = buildStatus()
    memcache.add(key='status',value=result,time=600)
    return result

def RefreshStatus():
    old_status = memcache.get('status')
    status = buildStatus()
    memcache.add(key='status',value=status,time=600)
    if old_status is None or old_status['beacon'] != status['beacon']:
        "things changed so maybe tweet or something"

class MainPage(webapp2.RequestHandler):
    def get(self):
        status = getStatus()
        if isDev():
            status = {k:re.sub(r"[^\w-]","",self.request.get(k,v)) for k,v in status.iteritems()}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(status))

class RefreshHandler(webapp2.RequestHandler):
    def get(self):
        RefreshStatus()
        self.response.write("u did the thing")

class StatusJson(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(getStatus()))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin/refresh', RefreshHandler),
    ('/v0/status.json', StatusJson),
    ], debug=True)
