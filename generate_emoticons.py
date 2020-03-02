from emot.emo_unicode import EMOTICONS
import nltk
from emotion_lexicon import emolex_words
import operator
import json

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

emoticons_emotion = {}

for k, v in EMOTICONS.items():
    words = nltk.word_tokenize(v)
    for e in EMOTIONS:
        weight = {emotion: 0 for emotion in EMOTIONS}
    for word in words:
        result = emolex_words[emolex_words.word == word]
        if result.empty:
            continue
        for e in NRC_EMOTIONS:
            weight[TAGS[e]] += int(getattr(result, e))
    max_emotion = max(weight.items(), key=operator.itemgetter(1))[0]
    if weight[max_emotion] == 0:
        continue
    emoticons_emotion[k] = max_emotion

with open('emoticons_emotion.json', 'w') as f:
    f.write(json.dumps(emoticons_emotion, ensure_ascii=False))
