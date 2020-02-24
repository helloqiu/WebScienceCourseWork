import twitter
import json
import logging
from pymongo import MongoClient
from urllib.parse import quote_plus

from emotion_lexicon import emolex_words
from utils import get_config

# setup the logging module
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

UK_BOUNDS = ['-7.57216793459, 49.959999905', '1.68153079591, 58.6350001085']

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience_course_work
collection = db.raw_tweet

api = twitter.Api(consumer_key=config['consumer_key'],
                  consumer_secret=config['consumer_secret'],
                  access_token_key=config['access_token_key'],
                  access_token_secret=config['access_token_secret'],
                  sleep_on_rate_limit=True)

stream = api.GetStreamFilter(languages=['en'], locations=UK_BOUNDS)

total = 0

while True:
    tweet = next(stream)
    total += 1
    try:
        # store the tweet
        collection.insert_one(tweet)
    except Exception as e:
        logging.error(e)
    print("\033[1A")
    print("\033[K")
    print(f'Total Number of Tweets: {total}')
