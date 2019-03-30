import os
import shutil
from elasticsearch import Elasticsearch
es = Elasticsearch()

directory_in_str = "/home/prasad/tumblr/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    query = {
        "query": {
            "match_phrase": {
                "photos.original_size.url": filename
            }
        },
        "size": 0
    }
    resp = es.search(index="tumblr_likes_3", body=query)
    if resp["hits"]["total"] == 0:
        print(filename)
        shutil.move(directory_in_str + filename, "extra")
