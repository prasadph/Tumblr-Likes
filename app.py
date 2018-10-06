import io
from datetime import datetime

from elasticsearch import Elasticsearch
from flask import Flask, send_file
from flask import render_template, request, url_for

from config import image_repo, index

app = Flask(__name__)
es = Elasticsearch()


@app.route("/photos/<code>")
def local_pic(code):
    if code.endswith("png"):
        mime = "image/png"
    elif code.endswith("jpg") or code.endswith("jpeg"):
        mime = "image/jpg"
    elif code.endswith("gif"):
        mime = "image/gif"
    with open(image_repo + code, 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype=mime
        )


@app.template_filter('local')
def get_local_url_pic(url):
    f = "/photos/"
    return f + url.rsplit('/', 1)[-1]


@app.route("/post/<code>")
def blog(code):
    post = es.get(index=index, doc_type="_doc", id=code)
    post = post["_source"]
    return render_template('home.html', post=post)


@app.route("/likes")
def likes():
    size = 20
    timestamp = int(request.args.get("timestamp", datetime.now().timestamp()))
    search = request.args.get("search", "")
    offset = int(request.args.get("offset", 0))
    blog_name = request.args.get("blog_name", None)
    tag = request.args.get("tag", None)

    posts = es.search(index=index, doc_type="_doc",
                      body=generate_body(offset=offset, search=search, size=size, timestamp=timestamp,
                                         blog_name=blog_name, tag=tag))
    count = posts['hits']['total']
    posts = [post["_source"] for post in posts["hits"]["hits"]]
    args = request.args.copy()

    if search:
        args["search"] = search
    args['offset'] = offset + size
    next_link = url_for(request.endpoint, **args)
    args['offset'] = offset - size
    prev_link = url_for(request.endpoint, **args)
    title = search
    blogs = get_all_blogs()

    # print(tags)
    # print(blogs)
    return render_template(
        'blog.html',
        posts=posts,
        prev=prev_link,
        next=next_link,
        search=search,
        title=title,
        count=count,
        size=size,
        offset=offset,
        blogs=blogs,
        blog_name=blog_name
    )


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
