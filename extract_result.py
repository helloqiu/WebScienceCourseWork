from pymongo import MongoClient
from urllib.parse import quote_plus
from utils import get_config, get_extended_text_or_text

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience
marked_tweet = db.marked_tweet
result = db.tweet_result

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
        result_tweet = {
            'emotion': emotion,
            'text': text,
            'original_tweet': tweet
        }
        result.insert_one(result_tweet)
        count += 1
    print(f'output {count} {emotion} tweets')
