from utils import get_config, remove_url, remove_username, translate_emo, correct_slang, get_extended_text_or_text
from pymongo import MongoClient
from urllib.parse import quote_plus
import nltk
import progressbar

config = get_config()

uri = "mongodb://%s:%s@%s" % (quote_plus(
    config['mongo_username']), quote_plus(
        config['mongo_password']), quote_plus(config['mongo_host']))

client = MongoClient(uri)
db = client.webscience
raw_tweet = db.raw_tweet
processed_tweet = db.processed_tweet

processed_tweet.create_index("id")
processed_tweet.create_index("text")

count = raw_tweet.estimated_document_count()
i = 0

with progressbar.ProgressBar(max_value=count, redirect_stdout=True) as bar:
    for tweet in raw_tweet.find():
        # update progress
        bar.update(i)
        i += 1

        # get text
        if 'text' not in tweet.keys():
            continue
        # use extended text for extended tweets
        text = get_extended_text_or_text(tweet)
        if text is None:
            continue
        # use original text or extended text for retweets
        if 'retweeted_status' in tweet.keys():
            original_text = get_extended_text_or_text(
                tweet['retweeted_status'])
            if original_text is not None:
                text = original_text

        # ignore tweets with same id
        if processed_tweet.count_documents({'id': tweet['id']}) > 0:
            continue
        # ignore tweets with same text content
        if processed_tweet.count_documents({'text': text}) > 0:
            continue

        content = text
        content = content.lower()
        content = remove_url(content)
        content = remove_username(content)
        emoticons = translate_emo(content)
        tweet['emoticons'] = emoticons
        content = content.lower().strip()
        words = nltk.word_tokenize(content)
        processed_words = []
        for w in words:
            processed_words.append(correct_slang(w))
        processed_text = ' '.join(processed_words)
        tweet['processed_text'] = processed_text
        processed_tweet.insert_one(tweet)
