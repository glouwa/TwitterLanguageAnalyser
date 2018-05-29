import tweepy
import unicodecsv as  csv

consumer_key = 'EPZx1r8VVkbrtLxxfqwaGCEok'
consumer_secret = '4TTj1xE9gD80muMcXVbjq3o4zaP9MkJvIMCYvkESEWEdmIEK1v'
access_token = '1000680515408683008-XATYWEZHtJvTNlRSd0suLpvZH2TJYN'
access_token_secret = 'TOAPgIIp3GsNXPGCwRWDXLqBmBLDMOWfQg9T60hOGSVuM'

consumer_key1 = 'V6tThVc9W8SHxcCemHoxvBCpu'
consumer_secret1 = 'tHAdc255ukdTiQlgu2ScDsNcMdN19hwxMH38AZCgRlJABs54Jj'
access_token1 = '1000699980087267330-gLDPsw7NuYl2zA31DNwZhLXpWe8tvi'
access_token_secret1 = 'MT3TVDHiFoVOf0fI4oggLLgXpad1cBIDaD3Znv0H0UQqN'

consumer_key1 = '2txDFLO3JRcivufznuRJZWZKO'
consumer_secret1 = 'PBHCAuuWafmzz05hyj8zjIEVQUsgzQozWXo6V3AZcwLcr3pArj'
access_token1 = '1000730493434855424-lZU6guxqzbNFJ2LIwjnPCe9Dgny1dz'
access_token_secret1 = 'F6LxC7Bj4tAvcTwhEjzPVJbpQmMxk1QkUCnUQVE64c8s3'

auth = tweepy.OAuthHandler(consumer_key1, consumer_secret1)
auth.set_access_token(access_token1, access_token_secret1)
api = tweepy.API(auth)

hashtag = "worldcup" #"ЧМ2018"

tweets = tweepy.Cursor(api.search, q=hashtag, lang='en').items(1000)

with open('tweets.csv', 'a') as outfile:
    writer = csv.writer(outfile)
    #writer.writerow(['hashtag','timestamp', 'text', 'lang'])
    for tweet in tweets:
        writer.writerow([hashtag, tweet.created_at, tweet.text, tweet.lang])
