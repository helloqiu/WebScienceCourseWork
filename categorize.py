import json
import operator
from emotion_lexicon import emolex_words

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

with open('tweet.json', 'r') as f:
    tweets = json.loads(f.read())

count = {emotion: 0 for emotion in EMOTIONS}

for tweet in tweets:
    weight = {emotion: 0 for emotion in EMOTIONS}
    tags = [t['text'].lower() for t in tweet['entities']['hashtags']]
    for tag in tags:
        tag = tag.lower()
        word = emolex_words[emolex_words.word == tag]
        if word.empty:
            continue
        for e in NRC_EMOTIONS:
            weight[TAGS[e]] += int(getattr(word, e))
    max_emotion = max(weight.items(), key=operator.itemgetter(1))[0]
    if max(weight.values()) == 0:
        continue
    count[max_emotion] += 1
    print(f'Tweet text: {tweet["text"]}')
    print(f'Hashtags: {tags}')
    print(f'Weights: {weight}')
    print(f'Max Emotion: {max_emotion}')
    print('=' * 100)

print(count)
