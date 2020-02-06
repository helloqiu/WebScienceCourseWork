import twitter
import json
import logging
from pymongo import MongoClient
from urllib.parse import quote_plus

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

UK_BOUNDS = ['-7.57216793459, 49.959999905', '1.68153079591, 58.6350001085']

HASHTAGS_DICT = {
    'excitement': ('excitement', ),
    'happy': ('happy', 'joy', 'love'),
    'pleasant': ('pleasant', ),
    'surprise': ('surprise', 'sad', 'frustration'),
    'fear': ('fear', 'disgust', 'depression'),
    'angry': ('angry', ),
}

HASHTAGS = []
for i in HASHTAGS_DICT.keys():
    for j in HASHTAGS_DICT[i]:
        HASHTAGS.append(j)
print(HASHTAGS)


def get_config():
    with open('config.json', 'r') as f:
        return json.loads(f.read())


config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience_course_work
collection = db.tweet

api = twitter.Api(consumer_key=config['consumer_key'],
                  consumer_secret=config['consumer_secret'],
                  access_token_key=config['access_token_key'],
                  access_token_secret=config['access_token_secret'],
                  sleep_on_rate_limit=True)

stream = api.GetStreamFilter(languages=['en'], locations=UK_BOUNDS)
result = []

while True:
    tweet = next(stream)
    # ignore tweets that don't have hashtags
    if not tweet['entities']['hashtags']:
        logging.debug('Got a tweet which does not have hashtags.')
        continue

    tags = [t['text'].lower() for t in tweet['entities']['hashtags']]
    logging.info(f'Got a tweet which has hashtags: {tags}')
    for hashtag in HASHTAGS:
        filtered_tags = list(filter(lambda x: hashtag in x, tags))
        if filtered_tags:
            logging.info(
                f'\tFind hashtags: "{filtered_tags}"\n\tAll hashtags: {tags}')
            collection.insert_one(tweet)

#with open('result.json', 'a') as f:
#    f.write(json.dumps(result, ensure_ascii=False))
