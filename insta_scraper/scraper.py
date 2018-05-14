import requests, json, pprint
from lxml import html

urls = [
    'https://instagram.userlocal.jp/?page=1',
    'https://instagram.userlocal.jp/?page=2',
    'https://instagram.userlocal.jp/?page=3',
    'https://instagram.userlocal.jp/?page=4',
    'https://instagram.userlocal.jp/?page=5',
]

r = requests.get(urls[0])
tree = html.fromstring(r.text)

names = tree.xpath('//td/h4/a/text()')
hrefs = tree.xpath('//td/h4/a/@href')

name_url_js = {x: {'idx': names.index(x), 'url': y} for x, y in zip(names, hrefs)}
js = {}

for n in names:
    temp_r = requests.get(name_url_js[n]['url'])
    temp_tree = html.fromstring(temp_r.text)
    js[n] = {}
    js[n]['hashtag'] = temp_tree.xpath('//div/div/span/text()')
    js[n]['idx'] = name_url_js[n]['idx']

print (js)
