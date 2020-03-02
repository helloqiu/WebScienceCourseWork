from utils import get_config, remove_url, remove_username, translate_emo, correct_slang
from pymongo import MongoClient
from urllib.parse import quote_plus
import nltk
import progressbar

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience_course_work
raw_tweet = db.raw_tweet_with_keywords
processed_tweet = db.processed_tweet_with_keywords

count = raw_tweet.estimated_document_count()
i = 0

with progressbar.ProgressBar(max_value=count, redirect_stdout=True) as bar:
    for tweet in raw_tweet.find():
        # update progress
        bar.update(i)
        i += 1

        if 'text' not in tweet:
            continue

        if processed_tweet.count_documents({'id': tweet['id']}) > 0:
            continue

        content = tweet['text']
        content = content.lower()
        content = remove_url(content)
        content = remove_username(content)
        content = translate_emo(content)
        content = content.lower().strip()
        words = nltk.word_tokenize(content)
        processed_words = []
        for w in words:
            processed_words.append(correct_slang(w))
        processed_text = ' '.join(processed_words)
        tweet['processed_text'] = processed_text
        #print(tweet['text'])
        #print(processed_text)
        processed_tweet.insert_one(tweet)
