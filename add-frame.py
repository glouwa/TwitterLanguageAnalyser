import json
import pickle
import datetime
import iso3166

import pandas as pd
import numpy as np

with open('array-sent.json', 'r') as infile:
    tweets_in = json.load(infile)

error_rows = []

data_cols = ['time_ms', 'coord_x', 'coord_y', 'is_retweet', 'retweet_count', 'sentiment', 'anger', 'joy', 'sadness', 'fear', 'surprise', 'time', 'lang', 'loc', 'iso3166a2', 'iso3166a3', 'txt', 'user' ]
data = np.zeros((len(tweets_in), len(data_cols)), dtype=object)

for idx, tweet in enumerate(tweets_in):
    try:        
        data[idx, 0] = int(tweet['timestamp_ms'])
        data[idx, 1] = float(tweet['coordinates'][0])
        data[idx, 2] = float(tweet['coordinates'][1])        
        data[idx, 3] = int(tweet['text'].startswith('RT'))
        data[idx, 4] = int(tweet['retweet_count'])
        data[idx, 5] = float(tweet['sentiment'])
        data[idx, 6] = float(tweet['emotion']['anger'])
        data[idx, 7] = float(tweet['emotion']['joy'])
        data[idx, 8] = float(tweet['emotion']['sadness'])
        data[idx, 9] = float(tweet['emotion']['fear'])
        data[idx, 10] = float(tweet['emotion']['surprise'])
        data[idx, 11] = datetime.datetime.fromtimestamp(int((tweet['timestamp_ms']))/1000.0)
        data[idx, 12] = tweet['lang']
        data[idx, 13] = tweet['geo']
        
        split = tweet['geo'].split(',')        
        if len(split) == 3:            
            iso3166a2 = split[2].strip()            
            data[idx, 14] = iso3166a2

            iso3166a3 = iso3166.countries_by_alpha2[iso3166a2].alpha3            
            data[idx, 15] = iso3166a3            
        else:
            error_rows.append(idx)    
        
        data[idx, 16] = tweet['text']
        data[idx, 17] = tweet['user']['screen_name']    

    except KeyError as e:
        print("ERROR: {}".format(e))
        error_rows.append(idx)
        
panda = pd.DataFrame(data, columns=data_cols)
panda.drop(error_rows)
print(" {} droped".format(len(error_rows)))
print(" {} ok".format(len(panda)))
panda.to_pickle('first-game-panda-frame.pkl')
panda.to_csv('first-game-panda-frame.csv')