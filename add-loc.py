import json

from geopy import geocoders  
from geopy import exc
from urllib3 import exceptions

gn = geocoders.GeoNames(username='glouwa')

with open('cache-loc.json', 'r') as infile:
    cache = json.load(infile)

def processTweet(tweet):        
    loc = None
    if tweet['place']:
        loc = tweet['place']
    if tweet['coordinates']:
        loc = tweet['coordinates']
    if tweet['user']['location']:
        loc = tweet['user']['location']
    if loc:
        loc_str = str(loc)
        try:     
            if loc_str not in cache:
                geoloc = gn.geocode(loc)
                if geoloc:
                    cache[loc_str] = {
                        "address": geoloc.address,
                        "coord": [geoloc.longitude, geoloc.latitude]
                    }
                else:
                    cache[loc_str] = None
                
            else:
                geoloc = cache[loc_str]

            if loc_str in cache and cache[loc_str] != None:
                tweet['geo'] = cache[loc_str]['address']
                tweet['coordinates'] = cache[loc_str]['coord']
                tweets_out.append(tweet)
                
        except (exc.GeocoderTimedOut, exceptions.ReadTimeoutError, exceptions.ProtocolError):
            print("IOError")
        
tweets_out = []

with open('stream-raw-with-geo2.json', 'r') as infile:
    tweets_in = json.load(infile)

print(len(tweets_in))
langs = ['ar', 'nl', 'en', 'fr', 'de', 'it', 'ja', 'pt', 'ru', 'es']

for idx, tweet in enumerate(tweets_in):
    if idx % 5 == 0:        
        if  str(tweet['lang']) in langs:
            if idx % 100 == 0:
                print(idx, len(cache), len(tweets_out))
            processTweet(tweet)

            if idx % 100 == 0:
                with open('cache-loc.json', 'w') as outfile:
                    json.dump(cache, outfile)

            if idx % 1000 == 0:        
                with open('array-loc.json', 'w') as outfile:
                    json.dump(tweets_out, outfile)
