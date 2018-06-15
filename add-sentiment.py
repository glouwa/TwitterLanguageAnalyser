import json
import html

import indicoio

indicoio.config.api_key = 'c4d4e9597ef31b91c9e723ebcf363cdf'

tweets_out = []

with open('array-loc.json', 'r') as infile:
    tweets_in = json.load(infile)

tweets_out = {}

print(len(tweets_in))
act_langs = {}
data = {}

for idx, tweet in enumerate(tweets_in):
    if tweet['coordinates']:
        l = tweet['lang'] 
        if l:        
            act_langs[l] = act_langs.get(l, 0) + 1
            tweets_out[str(tweet['id'])] = tweet
            if l not in data:
                data[l] = {
                    "id": [],
                    "txt": []
                }
        
for idx, tweet in enumerate(tweets_in):
    if tweet['coordinates']:
        l = tweet['lang'] 
        if l:
            data[l]['id'].append(str(tweet['id']))
            data[l]['txt'].append(html.unescape(tweet['text']))
            
print(act_langs)

for k, v in data.items():
    sent = indicoio.sentiment(data[k]['txt'], language=k)
    emo = indicoio.emotion(data[k]['txt'], language=k)
    for idx, s in enumerate(sent):
        tweets_out[data[k]['id'][idx]]['sentiment'] = s
        tweets_out[data[k]['id'][idx]]['emotion'] = emo[idx]


with open('array-sent.json', 'w') as outfile:
    json.dump(tweets_in, outfile, indent=4) # save tweets in to keep order

#indicoio.sentiment(['indico is so easy to use!', 'Still really easy, yiss'], language='')