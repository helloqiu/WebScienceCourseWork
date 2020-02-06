import twitter
import json

UK_BOUNDS = ['-7.57216793459, 49.959999905', '1.68153079591, 58.6350001085']


def get_config():
    with open('config.json', 'r') as f:
        return json.loads(f.read())


config = get_config()

api = twitter.Api(consumer_key=config['consumer_key'],
                  consumer_secret=config['consumer_secret'],
                  access_token_key=config['access_token_key'],
                  access_token_secret=config['access_token_secret'],
                  sleep_on_rate_limit=True)

stream = api.GetStreamFilter(languages=['en'], locations=UK_BOUNDS)
result = []

for i in range(0, 10):
    result.append(next(stream))

with open('result.json', 'a') as f:
    f.write(json.dumps(result, ensure_ascii=False))
