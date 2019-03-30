import logging
import os
import pprint
import time

import pytumblr
import requests
from elasticsearch import Elasticsearch

from config import tumblr_config, image_repo, host
from core.elasticsearch.elastic import get_max_elastic_id, save_like

logging.basicConfig(filename='logs/tumblr_index.log', level=logging.DEBUG)

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    *tumblr_config
)
es = Elasticsearch(host=host)

limit = 50
# Tumblr API give max 50 likes when used with after parameter

pp = pprint.PrettyPrinter(indent=4)


def update_likes():
    count = limit
    offset = get_max_elastic_id()

    if offset:
        offset = int(offset) // 1000 - 1
    else:
        offset = 1
    print(offset)

    i = 0
    while count >= limit:
        time.sleep(3)
        posts = fetch_likes(offset)
        for like in posts['liked_posts']:
            i += 1
            process_like(like)
        if len(posts["liked_posts"]) == 0:
            break
        offset = posts["liked_posts"][-1]["liked_timestamp"] - 1
        count = len(posts['liked_posts'])
        logging.debug("new timestamp " + str(offset) + " " + str(count))
    print("indexed " + str(i) + " posts")


def fetch_likes(offset):
    posts = client.likes(limit=limit, after=offset)
    posts["liked_posts"] = sorted(posts["liked_posts"], key=lambda x: x[
        "liked_timestamp"], reverse=False)
    return posts


def process_like(like):
    print(like["liked_timestamp"], like["tags"],
          like["post_url"], like["summary"])
    if like.get("photos"):
        process_images_list(like["photos"])
    else:
        # write code to process videos and other types
        pass
    response = save_like(like)
    logging.debug(str(response["result"]) + " %d" %
                  like["liked_timestamp"])


def process_images_list(photos):
    for photo in photos:
        # print(photo["original_size"]['url'])
        url = photo["original_size"]['url']
        filename = image_repo + url.rsplit('/', 1)[1]
        if not os.path.isfile(filename):
            save_image(url, filename)


def save_image(url, filename):
    logging.info("Downloading %s" % url)
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)


if __name__ == '__main__':
    update_likes()
