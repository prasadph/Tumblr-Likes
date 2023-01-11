import os
import shutil
from elasticsearch import Elasticsearch
from config import tumblr_config, image_repo, host
from pyquery import PyQuery as pq
import hashlib
from sync import save_image
from config import tumblr_config, image_repo, host, index
import os
es = Elasticsearch(host=host)

# directory_in_str = "/home/prasad/tumblr/"
# directory = os.fsencode(directory_in_str)
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     query = {
#         "query": {
#             "match_phrase": {
#                 "photos.original_size.url": filename
#             }
#         },
#         "size": 0
#     }
#     resp = es.search(index="tumblr_likes_3", body=query)
#     if resp["hits"]["total"] == 0:
#         print(filename)
#         shutil.move(directory_in_str + filename, "extra")
query = {
    "query": {
        "bool": {
            "must_not":{
                 "bool": {
            "should": [
              {
                "match_phrase": {
                  "type.keyword": "photo"
                }
              },
              {
                "match_phrase": {
                  "type.keyword": "video"
                }
              },
              {
                "match_phrase": {
                  "type.keyword": "link"
                }
              },
              {
                "match_phrase": {
                  "type.keyword": "answer"
                }
              }
            ],
            "minimum_should_match": 1
          }

            }
        }
    },
    "size":10000,
    # "from":0,
}

resp = es.search(index=index, body=query)
print(len(resp['hits']['hits']))
for post in resp['hits']['hits']:
    if post['_source'].get('body'):
        figure = post['_source']['body']
        f = pq(figure)
        for image in f("img"):
            src = image.get("src")
            filename = image_repo + src.rsplit('/', 1)[1]
            if "media.tumblr.com" not in src: 
                m = hashlib.shake_128(str.encode(src)).hexdigest(5)
                filename = image_repo + str(m)+"-" +src.rsplit('/', 1)[1]
                # print(filename)
                pass
        # print(figure)
            
            if not os.path.isfile(filename):
                print(src, filename)
                save_image(src, filename)
    else:
        print(post['_source']['type'], "images_lost")