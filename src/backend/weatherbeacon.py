import json
import re
import os
import time

from google.appengine.api import memcache
from google.appengine.api import urlfetch

import jinja2
import webapp2
import yaml

from google.appengine.ext import vendor
vendor.add('lib')

import twitter


def rel(path):
    return os.path.join(os.path.dirname(__file__),path)

try:
    with open(rel("secrets.yaml")) as fh:
        config = yaml.load(fh)
except Exception as e:
    print e
    config = {}

if "twitter" in config:
    auth=twitter.OAuth( config['twitter']['access_token'],
                        config['twitter']['access_token_secret'],
                        config['twitter']['consumer_key'],
                        config['twitter']['consumer_secret'])
    t = twitter.Twitter(auth=auth)
    t_upload = twitter.Twitter(domain='upload.twitter.com',auth=auth)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(rel("templates")))

def isDev():
    # return False
    return os.environ.get('SERVER_SOFTWARE','').startswith('Development')

def getJson(url,cache_secs=None):
    mc_key = "url:"+url
    if cache_secs is not None:
        result = memcache.get(mc_key)
        if result is not None:
            return result
    result = json.loads(urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=0'}).content)
    if cache_secs is not None:
        memcache.set(key=mc_key,value=result,time=cache_secs)
    return result

def getForecast():
    url = "https://api.forecast.io/forecast/%s/%s,%s" % (config['forecast_io']['api_key'],config['weather']['lat'],config['weather']['lon'])
    return getJson(url,120)

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
    status = {
            'beacon': getSoxStatus() or weather,
            'weather': weather,
            'time': getSunClass(f['daily']['data'][0])
            }
    memcache.set(key='status',value=status,time=15*60)
    return status

def getStatus():
    if isDev():
        try:
            return getJson("https://weather-beacon.appspot.com/v0/status.json",60)
        except:
            return {'beacon': "clear", 'weather': "clear", 'time': "daytime"}
    result = memcache.get('status')
    if result is not None:
        return result
    result = buildStatus()
    return result

def tweetStatus(status):
    tweet_text = {
                'clear': "Steady blue, clear view",
                'cloudy': "Flashing blue, clouds due",
                'raining': "Steady red, rain ahead",
                'snowing': "Flashing red, snow instead",
                'sox-rainout': "Flashing red, the Sox game is cancelled",
                'sox-champs': "Flashing blue and red, the Boston Red Sox are world champions!"
            }[status['beacon']]
    t.statuses.update(status=tweet_text)
    # with open(rel("tweet_gifs/%s.gif"%status['beacon']),"rb") as fh:
    #     gif_data = fh.read()
    # gif_media_id = t_upload.media.upload(media=gif_data)["media_id_string"]
    # t.statuses.update(status=tweet_text, media_ids=gif_media_id)


def RefreshStatus():
    old_status = memcache.get('status')
    status = buildStatus()
    if old_status is None or old_status['beacon'] != status['beacon']:
        tweetStatus(status)

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
