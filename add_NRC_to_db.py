from emotion_lexicon import emolex_words
from utils import get_config
from pymongo import MongoClient
from urllib.parse import quote_plus

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience
collection = db.nrc
collection.create_index("word")

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

for _, w in emolex_words.iterrows():
    emotions = []
    for e in NRC_EMOTIONS:
        s = int(getattr(w, e))
        if s != 0:
            emotions.append(e)
    if len(emotions) != 0:
        collection.insert_one({'word': w.word, 'emotions': emotions})
