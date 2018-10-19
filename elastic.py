from config import index, doc_type
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

es = Elasticsearch()

def get_all_blogs():
    s = Search(using=es, index=index)
    s.aggs.bucket("per_blog","terms",field="blog_name.keyword",size=1000)
    response = s.execute()
 
    blogs = [blog.key for blog in response.aggregations.per_blog.buckets]
    return blogs

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

def fetch_post(code):
    return es.get(index=index, doc_type=doc_type, id=code)

def get_search_result(**params):
    s = Search(using=es, index=index)\
    .filter("range", liked_timestamp={"lt" :params["timestamp"]})\
    .filter(MultiMatch(query=params["search"],type="phrase_prefix",lenient=True))\
    .sort({"liked_timestamp":"desc"})
    if params.get("blog_name"):
        s=s.filter("term",blog_name__keyword=params.get("blog_name"))
    if params.get("tag"):
        s=s.filter("term",tags__keyword=params.get("tag"))
    print(s.to_dict())
    response = s[params["offset"]:params["size"]+params["offset"]].execute()
    return response
