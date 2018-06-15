import json
import pickle
import datetime

import pandas as pd
import numpy as np

with open('array-sent.json', 'r') as infile:
    tweets_in = json.load(infile)

error_rows = []

#cols = ['time', 'time_ms', 'lang', 'coord_x', 'coord_y', 'loc', 'txt', 'user', 'is_retweet', 'retweet_count', 'sentiment', 'anger', 'joy', 'sadness', 'fear', 'surprise' ]
data_cols = ['time_ms', 'coord_x', 'coord_y', 'is_retweet', 'retweet_count', 'sentiment', 'anger', 'joy', 'sadness', 'fear', 'surprise' ]
data = np.zeros((len(tweets_in), len(data_cols)))

for idx, tweet in enumerate(tweets_in):
    try:        
        data[idx, 0]  = int(tweet['timestamp_ms'])
        data[idx, 1]  = float(tweet['coordinates'][0])
        data[idx, 2]  = float(tweet['coordinates'][1])        
        data[idx, 3]  = tweet['text'].startswith('RT')
        data[idx, 4]  = int(tweet['retweet_count'])
        data[idx, 5] = float(tweet['sentiment'])
        data[idx, 6] = float(tweet['emotion']['anger'])
        data[idx, 7] = float(tweet['emotion']['joy'])
        data[idx, 8] = float(tweet['emotion']['sadness'])
        data[idx, 9] = float(tweet['emotion']['fear'])
        data[idx, 10] = float(tweet['emotion']['surprise'])
    except KeyError:
        error_rows.append(idx)
        
panda = pd.DataFrame(data, columns=data_cols)
panda.to_pickle('first-game-panda-frame.pkl')
panda.to_csv('first-game-panda-frame.csv')


data_cols = ['time', 'lang', 'loc', 'txt', 'user']
data = np.empty((len(tweets_in), len(data_cols)), dtype=object)
for idx, tweet in enumerate(tweets_in):
    try:
        data[idx, 0]  = datetime.datetime.fromtimestamp(int((tweet['timestamp_ms']))/1000.0)
        data[idx, 1]  = tweet['lang']
        data[idx, 2]  = tweet['geo']
        data[idx, 3]  = tweet['text']
        data[idx, 4]  = tweet['user']['screen_name']        
    except KeyError:
        error_rows.append(idx)
        
panda2 = pd.DataFrame(data, columns=data_cols)

panda2.to_pickle('first-game-panda-frame2.pkl')
panda2.to_csv('first-game-panda-frame2.csv')

panda3 = pd.concat([panda, panda2], axis=1)
panda3.drop(error_rows)

panda3.to_pickle('first-game-panda-frame3.pkl')
panda3.to_csv('first-game-panda-frame3.csv')