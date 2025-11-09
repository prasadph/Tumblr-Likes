import os
import shutil
from elasticsearch import Elasticsearch
from config import tumblr_config, image_repo, host, index
es = Elasticsearch(host=host)

query = {
    "query": {
        "match_all": {
        }
    }
}
resp = es.search(index=index, body=query, scroll="10m",
                 size=1000, _source="photos.original_size.url")
# print(resp)
# exit()
i = 1
while len(resp['hits']['hits']) > 0:
    for post in resp['hits']['hits']:
        if post["_source"].get("photos"):
            for photo in post["_source"]["photos"]:
                url = photo["original_size"]["url"]
                filename = image_repo + url.rsplit('/', 1)[1]
                if not os.path.isfile(filename):
                    print(filename)
    print(i)
    i += 1
    resp = es.scroll(scroll_id=resp["_scroll_id"], scroll="10m")
