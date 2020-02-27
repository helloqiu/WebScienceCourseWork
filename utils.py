import string
import re
from emot.emo_unicode import UNICODE_EMO, EMOTICONS
import json

URL = re.compile(
    r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
)
USERNAME = re.compile(r'@[a-zA-Z0-9_]{0,15}')

SLANG = {}
for s in string.ascii_lowercase:
    SLANG[s] = re.compile(s + r'{3,}')


def correct_slang(word):
    """
    correct the slang words
    """
    for s, v in SLANG.items():
        word = re.sub(v, s, word)
    return word


def remove_url(content):
    """`
    remove all urls from a sentence
    """
    content = re.sub(URL, '', content)
    return content


def remove_username(content):
    """
    remove all usernames from a sentence
    """
    content = re.sub(USERNAME, '', content)
    return content


def translate_emo(content):
    """
    translate all emojis and emoticons in a sentence
    """
    # translate unicode eomji to words
    for k, v in UNICODE_EMO.items():
        if k in content:
            content = re.sub(
                r'(' + k + ')',
                " ".join(v.replace(",", "").replace(":", "").split()) + " ",
                content)
    # translate emoticons to words
    for k, v in EMOTICONS.items():
        if k in content:
            content = content.replace(k, v)
    # replace unecessary chars
    content = content.replace("_", " ").replace("-", " ")
    return content


def get_config():
    """
    Read the config file.
    """
    with open('config.json', 'r') as f:
        return json.loads(f.read())
