import json
import re

# functions to tokenize tweets.
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

## Open file
f0 = open('pretty_tweets_raw.json', 'w+')
f1 = open('pretty_tweets_filtered.json', 'w+')
f2 = open('tweets_filtered_inline.json', 'w+')

known_ids = []

## Processing
with open('ColectedData/stream_data.json', 'r') as f:
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        f0.write(json.dumps(tweet, indent=4)) # pretty-print

        if 'retweeted_status' in tweet:
            tweet = tweet['retweeted_status']

        if tweet['id'] in known_ids:
            continue

        known_ids.append(tweet['id'])

        cleanTweet = {}
        cleanTweet['in_reply_to_status_id_str'] = tweet['in_reply_to_status_id_str']
        cleanTweet['in_reply_to_user_id'] = tweet['in_reply_to_user_id']
        cleanTweet['lang'] = tweet['lang']
        cleanTweet['text'] = tweet['text']
        cleanTweet['place'] = tweet['place']
        cleanTweet['id'] = tweet['id']
        cleanTweet['in_reply_to_user_id_str'] = tweet['in_reply_to_user_id_str']
        cleanTweet['created_at'] = tweet['created_at']
        cleanTweet['geo'] = tweet['geo']
        cleanTweet['is_quote_status'] = tweet['is_quote_status']
        cleanTweet['in_reply_to_status_id'] = tweet['in_reply_to_status_id']
        cleanTweet['coordinates'] = tweet['coordinates']
        # cleanTweet['timestamp_ms'] = tweet['timestamp_ms']

        newUser = {}
        newUser['screen_name'] = tweet['user']['screen_name']
        newUser['id'] = tweet['user']['id']
        newUser['location'] = tweet['user']['location']
        newUser['name'] = tweet['user']['name']

        cleanTweet['user'] = newUser

        token = preprocess(cleanTweet['text'])
        f1.write(json.dumps(cleanTweet, indent=4)) # pretty-print
        f2.write(str(cleanTweet) + "\n") # pretty-print
