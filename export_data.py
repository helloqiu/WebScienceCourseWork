from pymongo import MongoClient
from urllib.parse import quote_plus
from utils import get_config, get_extended_text_or_text
import csv

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience
marked_tweet = db.marked_tweet

EMOTIONS = [
    'excitement',
    'happy',
    'pleasant',
    'surprise',
    'fear',
    'angry',
]

for emotion in EMOTIONS:
    count = 0
    result = list()
    # choose tweets which 1 <= max_emotion_weight <= 2
    for tweet in marked_tweet.find({
            'emotion': emotion,
            'max_emotion_weight': {
                '$gte': 1,
                '$lte': 2
            }
    }):
        if count == 150:
            break
        text = get_extended_text_or_text(tweet)
        if text is None:
            continue
        # use original text or extended text for retweets
        if 'retweeted_status' in tweet.keys():
            original_text = get_extended_text_or_text(
                tweet['retweeted_status'])
            if original_text is not None:
                text = original_text
        result.append({
            'tweet_id': tweet['id'],
            'created_at': tweet['created_at'],
            'text': text
        })
    with open(f'{emotion}_result.csv', 'w', newline='') as csvfile:
        fieldnames = ['tweet_id', 'created_at', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(result)
