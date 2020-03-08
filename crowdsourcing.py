from pymongo import MongoClient
from urllib.parse import quote_plus
from utils import get_config
import random
import csv

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience
result = db.tweet_result

EMOTIONS = [
    'excitement',
    'happy',
    'pleasant',
    'surprise',
    'fear',
    'angry',
]

output = list()

for emotion in EMOTIONS:
    tweets = list(result.find({'emotion': emotion}))
    # get 20 samples for each emotion
    sample = random.sample(tweets, 20)
    output = output + [{
        'text': tweet['text'],
        'emotion': tweet['emotion'],
        'id': tweet['original_tweet']['id']
    } for tweet in sample]

with open('crowdsourcing_input.csv', 'w', newline='') as csvfile:
    fieldnames = ['text', 'emotion', 'id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(output)
