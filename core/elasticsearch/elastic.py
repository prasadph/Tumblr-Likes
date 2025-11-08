from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
from elasticsearch_dsl.query import MultiMatch

from config import index, doc_type, host

es = Elasticsearch(host=host)


def delete_like(post_id):
    es.delete(id=post_id, doc_type=doc_type, index=index)


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


def get_top_tags(limit=20):
    """Get top tags by count overall"""
    s = Search(using=es, index=index)
    s.aggs.bucket("tags", "terms", field="tags.keyword", size=limit, order={"_count": "desc"})
    response = s.execute()
    tags = []
    for bucket in response.aggregations.tags.buckets:
        tags.append({
            'name': bucket.key,
            'count': bucket.doc_count
        })
    return tags


def get_top_tags_recent(limit=20, days=30):
    """Get top tags by count from recent posts (last N days)"""
    from datetime import datetime, timedelta
    
    # Calculate timestamp for N days ago
    # liked_timestamp appears to be in seconds (not milliseconds)
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_timestamp = int(cutoff_date.timestamp())
    
    s = Search(using=es, index=index)
    s = s.filter("range", liked_timestamp={"gte": cutoff_timestamp})
    s.aggs.bucket("tags", "terms", field="tags.keyword", size=limit, order={"_count": "desc"})
    response = s.execute()
    tags = []
    for bucket in response.aggregations.tags.buckets:
        tags.append({
            'name': bucket.key,
            'count': bucket.doc_count
        })
    return tags


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
    # s = s.filter('nested', filter=Q('exists', field="tags"))
    # s = s.filter("exists",field="tags")
    # s = s.filter("bool",must_not=[Q('exists', field="tags")])
    # s = s.extra(search_after=['152881177616', 0])
    # s = s.filter("term", type__keyword="text")
    print(s.to_dict())
    response = s[params["offset"]:params["size"] + params["offset"]].execute()
    return response


def get_timestamp_range(**params):
    """Get min and max liked_timestamp for the current search/filter"""
    s = Search(using=es, index=index) \
        .filter("range", liked_timestamp={"lt": params["timestamp"]}) \
        .filter(MultiMatch(query=params["search"], type="phrase_prefix", lenient=True))
    if params.get("blog_name"):
        s = s.filter("term", blog_name__keyword=params.get("blog_name"))
    if params.get("tag"):
        s = s.filter("term", tags__keyword=params.get("tag"))
    
    # Add aggregations for min and max (using same pattern as get_max_elastic_id)
    s.aggs.bucket("min_ts", "min", field="liked_timestamp")
    s.aggs.bucket("max_ts", "max", field="liked_timestamp")
    
    s = s[:0]  # Don't return documents, just aggregations
    response = s.execute()
    
    min_ts = None
    max_ts = None
    
    if hasattr(response, 'aggregations') and response.aggregations:
        if hasattr(response.aggregations, 'min_ts') and response.aggregations.min_ts:
            min_ts = response.aggregations.min_ts.value
        if hasattr(response.aggregations, 'max_ts') and response.aggregations.max_ts:
            max_ts = response.aggregations.max_ts.value
    
    return {
        'min_timestamp': min_ts,
        'max_timestamp': max_ts
    }


def get_top_tags_for_search(limit=5, **params):
    """Get top tags by count for the current search/filter context"""
    s = Search(using=es, index=index) \
        .filter("range", liked_timestamp={"lt": params["timestamp"]}) \
        .filter(MultiMatch(query=params["search"], type="phrase_prefix", lenient=True))
    if params.get("blog_name"):
        s = s.filter("term", blog_name__keyword=params.get("blog_name"))
    if params.get("tag"):
        s = s.filter("term", tags__keyword=params.get("tag"))
    
    # Add aggregation for top tags
    s.aggs.bucket("tags", "terms", field="tags.keyword", size=limit, order={"_count": "desc"})
    
    s = s[:0]  # Don't return documents, just aggregations
    response = s.execute()
    
    tags = []
    if hasattr(response, 'aggregations') and response.aggregations:
        if hasattr(response.aggregations, 'tags') and response.aggregations.tags:
            for bucket in response.aggregations.tags.buckets:
                tags.append({
                    'name': bucket.key,
                    'count': bucket.doc_count
                })
    
    return tags
