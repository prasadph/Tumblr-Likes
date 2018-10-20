import logging
import os
import pprint
import time

import pytumblr
import requests
from elasticsearch import Elasticsearch

from config import tumblr_config, image_repo
from core.elasticsearch.elastic import get_max_id, save_like

logging.basicConfig(filename='tumblr_test2.log', level=logging.DEBUG)

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    *tumblr_config
)
es = Elasticsearch()

limit = 50

count = limit

pp = pprint.PrettyPrinter(indent=4)

offset = get_max_id()

if offset:
    offset = int(offset) // 1000 - 1
else:
    offset = 1
print(offset)

i = 0
while count >= limit:
    time.sleep(3)
    posts = client.likes(limit=limit, after=offset)
    posts["liked_posts"] = sorted(posts["liked_posts"], key=lambda x: x[
        "liked_timestamp"], reverse=False)

    for like in posts['liked_posts']:
        i += 1

        print(like["liked_timestamp"], like["tags"],
              like["post_url"], like["summary"])
        if like.get("photos"):
            for photo in like["photos"]:
                # print(photo["original_size"]['url'])
                url = photo["original_size"]['url']
                filename = image_repo + url.rsplit('/', 1)[1]
                if not os.path.isfile(filename):
                    logging.debug("Downloading %s" % url)
                    r = requests.get(url, allow_redirects=True)
                    open(filename, 'wb').write(r.content)
        else:
            pass
        response = save_like(like)
        logging.debug(str(response["result"]) + " %d" %
                      like["liked_timestamp"])
    if len(posts["liked_posts"]) == 0:
        break
    offset = posts["liked_posts"][-1]["liked_timestamp"] - 1
    count = len(posts['liked_posts'])
    logging.debug("new timestamp " + str(offset) + " " + str(count))
print("indexed " + str(i) + " posts")
