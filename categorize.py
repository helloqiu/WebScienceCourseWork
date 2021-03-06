import json
import operator
from emotion_lexicon import emolex_words
from pymongo import MongoClient
from urllib.parse import quote_plus
from utils import get_config
import nltk
import progressbar

TEXT_SCORE = 0.5
TAG_SCORE = 3.0
EMOTICON_SCORE = 3.0

TAGS = {
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

NRC_EMOTIONS = list(TAGS.keys())
EMOTIONS = [
    'excitement',
    'happy',
    'pleasant',
    'surprise',
    'fear',
    'angry',
]

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience
processed_tweet = db.processed_tweet
marked_tweet = db.marked_tweet
nrc = db.nrc

marked_tweet.create_index("id")

count = processed_tweet.estimated_document_count()
i = 0

with progressbar.ProgressBar(max_value=count, redirect_stdout=True) as bar:
    for tweet in processed_tweet.find():
        bar.update(i)
        i += 1

        if marked_tweet.count_documents({'id': tweet['id']}) > 0:
            continue

        weight = {emotion: 0 for emotion in EMOTIONS}
        # marking based on text content
        content = tweet['processed_text']
        # words = nltk.word_tokenize(content)
        words = content.split(' ')
        for word in words:
            result = nrc.find_one({'word': word})
            if not result:
                continue
            for e in result['emotions']:
                weight[TAGS[e]] += TEXT_SCORE
        # marking based on tags
        if 'entities' in tweet.keys() and 'hashtags' in tweet['entities']:
            tags = [t['text'].lower() for t in tweet['entities']['hashtags']]
            for tag in tags:
                tag = tag.lower()
                result = nrc.find_one({'word': tag})
                if not result:
                    continue
                for e in result['emotions']:
                    weight[TAGS[e]] += TAG_SCORE
        # marking based on emoticons
        for emoticon in tweet['emoticons']:
            weight[emoticon] += EMOTICON_SCORE

        max_emotion = max(weight.items(), key=operator.itemgetter(1))[0]
        tweet['emotions_weight'] = weight
        tweet['emotion'] = max_emotion
        tweet['max_emotion_weight'] = weight[max_emotion]
        if weight[max_emotion] == 0:
            # ignore tweets which have 0 marks
            continue
        marked_tweet.insert_one(tweet)
