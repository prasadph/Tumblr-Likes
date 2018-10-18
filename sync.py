import logging
import pprint
import time
import pytumblr
import os
from elasticsearch import Elasticsearch
from config import tumblr_config, index, image_repo
import requests
from datetime import datetime
import json
logging.basicConfig(filename='tumblr_test2.log', level=logging.DEBUG)

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
    "size": 0
}
response = es.search(index=index, body=body, doc_type="_doc")
offset = response["aggregations"]["maxm"]["value"]

if offset:
    offset = int(offset) // 1000 - 1
else:
    offset = 1
print(offset)
# print(datetime.utcfromtimestamp(offset/1000).strftime('%Y-%m-%d %H:%M:%S'))
# # posts = client.likes(limit=limit, before=offset/1000)
# posts = client.likes(limit=limit, before=datetime.now().timestamp())
# print(posts["liked_posts"][-1])
# exit()
i = 0
while count >= limit:
    time.sleep(3)
    # before=datetime.now().timestamp()
    posts = client.likes(limit=limit, after=offset)
    # pp.pprint(posts)
    # exit()
    # print(posts["liked_posts"][0]["timestamp"])
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
                pass
        else:
            pass
        response = es.index(index=index, doc_type="_doc",
                            id=like["id"], body=like)
        logging.debug(str(response["result"]) + " %d" %
                      like["liked_timestamp"])
    if (len(posts["liked_posts"]) == 0):
        break
    offset = posts["liked_posts"][-1]["liked_timestamp"] - 1
    count = len(posts['liked_posts'])
    logging.debug("new timestamp " + str(offset) + " " + str(count))
print("indexed " + str(i) + " posts")
