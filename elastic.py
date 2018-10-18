from config import index
from elasticsearch import Elasticsearch

es = Elasticsearch()
def get_all_blogs():
    body = {
        "aggs": {
            "blogs": {
                "terms": {
                    "field": "blog_name.keyword",
                    "size": 1000
                }
            }
        },
        "size": 0,
    }
    blogs = es.search(index=index, body=body)[
        "aggregations"]["blogs"]["buckets"]
    return [blog["key"] for blog in blogs]

def get_all_tags():
    body = {
        "aggs":
            {
                "tags": {
                    "terms": {
                        "field": "tags.keyword",
                        "size": 1000
                    }
                }},
        "size": 0}
    blogs = es.search(index=index, body=body)[
        "aggregations"]["tags"]["buckets"]
    return [tag["key"] for tag in blogs]


def generate_body(**params):
    body = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        },
        "from": params['offset'],
        "size": params['size'],
        "sort": {"liked_timestamp": "desc"}
    }
    if params['search']:
        body["query"]["bool"]["filter"].append({
            "multi_match": {
                "type": "phrase_prefix",
                "query": params['search'],
                "lenient": True
            }
        })

    body["query"]["bool"]["must"].append({
        "range": {
            "liked_timestamp": {
                "lt": params['timestamp']
            }
        }
    })
    if params.get('blog_name'):
        body["query"]["bool"]["filter"].append({
            "term": {
                "blog_name.keyword": {
                    "value": params["blog_name"]
                }
            }
        })
    if params.get('tag'):
        body["query"]["bool"]["filter"].append({
            "term": {
                "tags.keyword": {
                    "value": params["tag"]
                }
            }
        })
    print(body)
    return body

def fetch_post(code):
    return es.get(index=index, doc_type="_doc", id=code)

def get_search_result(offset, search, size, timestamp, blog_name, tag):
     return es.search(index=index, doc_type="_doc",
                      body=generate_body(offset=offset, search=search, size=size, timestamp=timestamp,
                                         blog_name=blog_name, tag=tag))