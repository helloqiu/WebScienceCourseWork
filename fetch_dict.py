from bs4 import BeautifulSoup
import requests, json
resp = requests.get("http://www.netlingo.com/acronyms.php")
soup = BeautifulSoup(resp.text, "html.parser")
slangdict = {}
key = ""
value = ""
for div in soup.findAll('div', attrs={'class': 'list_box3'}):
    for li in div.findAll('li'):
        for a in li.findAll('a'):
            key = a.text
            value = li.text.split(key)[1]
            key = key.lower()
            slangdict[key] = value

with open('slang.json', 'w') as f:
    json.dump(slangdict, f, indent=2)
