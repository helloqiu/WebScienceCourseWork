import twitter
import json
import logging
from pymongo import MongoClient
from urllib.parse import quote_plus

from emotion_lexicon import emolex_words
from utils import get_config

import argparse

# setup the logging module
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

UK_BOUNDS = ['-7.57216793459, 49.959999905', '1.68153079591, 58.6350001085']
KEYWORDS = [
    'excitement',
    'happy',
    'pleasant',
    'surprise',
    'fear',
    'angry',
]
NRC_KEYWORD_MAP = {
    'anger': 'angry',
    'disgust': 'fear',
    'fear': 'fear',
    'joy': 'happy',
    'sadness': 'surprise',
    'surprise': 'surprise',
    'negative': 'surprise',
    'positive': 'pleasant',
    'trust': 'pleasant',
    'anticipation': 'excitement',
}

# parse args to get the target emotion
parser = argparse.ArgumentParser(description='Tweets crawler.')
parser.add_argument('--emotion', type=str, nargs=1, choices=KEYWORDS)
args = parser.parse_args()

target_emotion = args.emotion[0]

logging.info(f'Fetching tweets with keyword "{target_emotion}"')

# connect to MongoDB
config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience
collection = db.raw_tweet

# get keywords from nrc lexicon
nrc = db.nrc
target_nrc_emotions = [
    i[0] for i in list(
        filter(lambda x: x[1] == target_emotion, NRC_KEYWORD_MAP.items()))
]
keywords = list(
    nrc.find({
        '$or': [{
            'emotions': e
        } for e in target_nrc_emotions]
    }).limit(400))
keywords = [w['word'] for w in keywords]

# create an index of "id"
collection.create_index("id")
# create an index of "text"
collection.create_index("text")

api = twitter.Api(consumer_key=config['consumer_key'],
                  consumer_secret=config['consumer_secret'],
                  access_token_key=config['access_token_key'],
                  access_token_secret=config['access_token_secret'],
                  sleep_on_rate_limit=True)

stream = api.GetStreamFilter(languages=['en'],
                             locations=UK_BOUNDS,
                             track=keywords)

total = 0

while True:
    tweet = next(stream)
    # ignore tweets with same id
    if 'id' not in tweet.keys() or collection.count_documents(
        {'id': tweet['id']}) > 0:
        continue
    # ignore tweets with same text content
    if 'text' not in tweet.keys() or collection.count_documents(
        {'text': tweet['text']}) > 0:
        continue

    total += 1
    tweet['track_with'] = target_emotion
    try:
        # store the tweet
        collection.insert_one(tweet)
    except Exception as e:
        logging.error(e)
    logging.info(f'Total Number of Tweets: {total}')
    # stop when total count reaches 10000
    if total == 10000:
        break
