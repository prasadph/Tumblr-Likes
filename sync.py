import logging
import pprint
import time
import pytumblr
import os
from elasticsearch import Elasticsearch
from config import tumblr_config, index, image_repo
import requests

index = "tumblr_likes"
logging.basicConfig(filename='tumblr_test.log', level=logging.DEBUG)

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    *tumblr_config
)
es = Elasticsearch()

limit = 50
offset = 1
count = limit

pp = pprint.PrettyPrinter(indent=4)

body = {
    "aggs": {
        "maxm": {
            "max": {"field": "liked_timestamp"}
        }
    },
    "size" :0
}
response = es.search(index=index, body=body, doc_type="_doc")
offset = response["aggregations"]["maxm"]["value"]
if offset:
    offset = int(offset)
else:
    offset = 0
print(offset)
while count >= limit:
    time.sleep(5)
    posts = client.likes(limit=limit, after=offset)
    # pp.pprint(posts)
    # print(posts["liked_posts"][0]["timestamp"])
    for like in posts['liked_posts']:
        response = es.index(index=index, doc_type="_doc", id=like["id"], body=like)
        print(like["liked_timestamp"], like["tags"], like["post_url"], like["summary"])
        if like.get("photos"):
            for photo in like["photos"]:
                # print(photo["original_size"]['url'])
                url = photo["original_size"]['url']
                filename = image_repo + url.rsplit('/', 1)[1]
                if not os.path.isfile(filename):
                    logging.debug("Downloading %s" % url)
                    r = requests.get(url, allow_redirects=True)        
                    open(filename, 'wb').write(r.content)
                pass
        else:
            pass
    if (len(posts["liked_posts"]) == 0):
        break
    offset = posts["liked_posts"][0]["liked_timestamp"]
    count = len(posts['liked_posts'])
    logging.debug("new timestamp " + str(offset) + " " + str(count))
