import io
from datetime import datetime

from flask import render_template, request, url_for
from flask import send_file

from app import app
from config import image_repo
from core.elasticsearch.elastic import get_all_blogs, get_search_result, fetch_post


@app.route("/likes")
def likes():
    size = 20
    timestamp = int(request.args.get("timestamp", datetime.now().timestamp()))
    search = request.args.get("search", "")
    offset = int(request.args.get("offset", 0))
    blog_name = request.args.get("blog_name", None)
    tag = request.args.get("tag", None)

    posts = get_search_result(offset=offset, search=search, size=size, timestamp=timestamp,
                              blog_name=blog_name, tag=tag)
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


@app.route("/post/<code>")
def blog(code):
    post = fetch_post(code)
    post = post["_source"]
    return render_template('home.html', post=post)


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