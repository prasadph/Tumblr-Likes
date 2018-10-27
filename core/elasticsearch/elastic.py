from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

from config import index, doc_type

es = Elasticsearch()


def delete_like(post_id):
    es.delete(post_id)


def get_max_elastic_id():
    s = Search(using=es, index=index)
    s.aggs.bucket("maxm", "max", field='liked_timestamp')
    response = s.execute()
    return response["aggregations"]["maxm"]["value"]


def save_like(like):
    return es.index(index=index, doc_type=doc_type, id=like["id"], body=like)


def get_all_blogs():
    s = Search(using=es, index=index)
    s.aggs.bucket("per_blog", "terms", field="blog_name.keyword", size=1000)
    response = s.execute()
    blogs = [blog.key for blog in response.aggregations.per_blog.buckets]
    return blogs


def get_all_tags():
    s = Search(using=es, index=index)
    s.aggs.bucket("tags", "terms", field="tags.keyword", size=1000)
    response = s.execute()
    return [tag.key for tag in response.aggregations.tags.buckets]


def fetch_post(code):
    return es.get(index=index, doc_type=doc_type, id=code)


def get_search_result(**params):
    s = Search(using=es, index=index) \
        .filter("range", liked_timestamp={"lt": params["timestamp"]}) \
        .filter(MultiMatch(query=params["search"], type="phrase_prefix", lenient=True)) \
        .sort({"liked_timestamp": "desc"})
    if params.get("blog_name"):
        s = s.filter("term", blog_name__keyword=params.get("blog_name"))
    if params.get("tag"):
        s = s.filter("term", tags__keyword=params.get("tag"))
    print(s.to_dict())
    response = s[params["offset"]:params["size"] + params["offset"]].execute()
    return response
