import json, os
import concurrent.futures

with open ('./celebrity_hashtags.json', 'r') as f:
    cele_json = json.load(f)

# hashtag list
hashes = []
for u in list(cele_json.keys()):
    hashes.append(cele_json[u]['hashtag'])
hashes = sum(hashes, [])

# parallel retriever
arr = [(idx, tag) for idx, tag in enumerate(hashes)]
def img_downloader(arr):
    idx, tag = arr
    dp = './imgs/test_0129/' + tag
    # fetch only media metadata
    command = 'instagram-scraper --tag {} -t none --media-metadata --include-location --comments --maximum 10'.format(tag)
    os.system (command)
    
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as e:
    e.map(img_downloader, arr)