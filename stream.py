import json
import tweepy
from geopy import geocoders  
from geopy import exc
from urllib3 import exceptions

gn = geocoders.GeoNames(username='glouwa')

consumer_key1        = '2txDFLO3JRcivufznuRJZWZKO'
consumer_secret1     = 'PBHCAuuWafmzz05hyj8zjIEVQUsgzQozWXo6V3AZcwLcr3pArj'
access_token1        = '1000730493434855424-lZU6guxqzbNFJ2LIwjnPCe9Dgny1dz'
access_token_secret1 = 'F6LxC7Bj4tAvcTwhEjzPVJbpQmMxk1QkUCnUQVE64c8s3'

auth = tweepy.OAuthHandler(consumer_key1, consumer_secret1)
auth.set_access_token(access_token1, access_token_secret1)
api = tweepy.API(auth)

tweets = []

class MyStreamListener(tweepy.StreamListener):    
    def on_status(self, tweet):
        loc = None
        if tweet.place:
            loc = tweet.place
        if tweet.coordinates:            
            loc = tweet.coordinates
        if tweet.user.location:
            loc = tweet.user.location
        if loc:       
            try:     
                geoloc = gn.geocode(loc)
                if geoloc:
                    text = tweet.text
                    if 'extended_tweet' in tweet._json and 'full_text' in tweet._json['extended_tweet']:
                        text = "++++++++++ " + tweet._json['extended_tweet']['full_text']
                    
                    #print(geoloc, (geoloc.latitude, geoloc.longitude))                    
                    #print(geoloc.address, [geoloc.longitude, geoloc.latitude])
                    tweet._json['geo'] = geoloc.address
                    tweet._json['coordinates'] = [geoloc.longitude, geoloc.latitude]

                    tweets.append(tweet._json)
                    if len(tweets) % 10 == 0:
                        with open('stream-raw-with-geo.json', 'w') as outfile:
                            json.dump(tweets, outfile)
                            print(len(tweets))
                    #print(json.dumps(tweet._json, indent=4))
                    #print("[{},{}],".format(geoloc.longitude, geoloc.latitude))
                    #print(text)
            except (exc.GeocoderTimedOut, exceptions.ReadTimeoutError, exceptions.ProtocolError):
                print("IOError")
    
        
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['worldcup', 'ЧМ2012', 'diemannschaft'], async=True)

print("start listening")


