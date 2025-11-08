import io
from datetime import datetime

from flask import render_template, request, url_for, jsonify
from flask import send_file
import core.tumblr.likes as tumblr_likes
from app import app
from config import image_repo, posts_per_page
from core.elasticsearch.elastic import get_all_blogs, get_search_result, fetch_post

template_root = "likes/"

@app.route("/test", methods=['GET'])
def test():
    
    return "test1"

@app.route("/api/unlike", methods=['POST'])
def unlike():

    if request.method == "POST" and request.is_json:
        ret = tumblr_likes.unlike(request.json["id"], request.json['reblog_key'])
        return jsonify(ret)


@app.route("/api/relike", methods=['POST'])
def relike():

    if request.method == "POST" and request.is_json:
        ret = tumblr_likes.relike(request.json["id"], request.json['reblog_key'])
        return jsonify(ret)


@app.route("/likes")
def likes():
    size = posts_per_page
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
    if tag:
        title=tag
    blogs = get_all_blogs()
    like = [[post["id"], post['reblog_key']] for post in posts]
    return render_template(
        template_root + 'blog.html',
        posts=posts,
        prev=prev_link,
        next=next_link,
        search=search,
        title=title,
        count=count,
        size=size,
        offset=offset,
        blogs=blogs,
        blog_name=blog_name,
        like_list=like,
    )


@app.route("/post/<code>")
def blog(code):
    post = fetch_post(code)
    post = post["_source"]
    return render_template(template_root + 'singlepost.html', post=post)


@app.route("/photos/<code>")
def local_pic(code):
    if code.endswith("png"):
        mime = "image/png"
    elif code.endswith("jpg") or code.endswith("jpeg"):
        mime = "image/jpg"
    elif code.endswith("gif"):
        mime = "image/gif"
    elif code.endswith("webp"):
        mime = "image/webp"
    #handle webp and others
    with open(image_repo + code, 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype=mime
        )


# TODO Not a view move to other file in future
@app.template_filter('local')
def get_local_url_pic(url):
    f = "/photos/"
    return f + url.rsplit('/', 1)[-1]


@app.template_filter('ttimages')
def get_modifed_body(body):
    from pyquery import PyQuery as pq
    
    f = pq(body)
    out = ""
    for image in f("img"):
            src = image.get("src")
            filename = "/photos/" + src.rsplit('/', 1)[1]
            if "media.tumblr.com" not in src: 
                import hashlib
                m = hashlib.shake_128(str.encode(src)).hexdigest(5)
                filename = "/photos/" + str(m)+"-" +src.rsplit('/', 1)[1]
            # Wrap each image in a container for proper styling and gallery
            out = out + f'<div class="post-image-container"><img src="{filename}" class="post-image" alt="Post image" loading="lazy"></div>'
                
    return out


@app.template_filter('relativetime')
def relative_time(timestamp):
    """Convert timestamp to relative time string using humanize"""
    if not timestamp:
        return "Unknown"
    
    try:
        import humanize
        
        # Handle both epoch seconds and epoch milliseconds
        if isinstance(timestamp, (int, float)):
            if timestamp > 1e10:  # Likely milliseconds
                timestamp = timestamp / 1000
            dt = datetime.fromtimestamp(timestamp)
        else:
            dt = timestamp
        
        return humanize.naturaltime(dt)
    except ImportError:
        # Fallback if humanize is not installed
        try:
            if isinstance(timestamp, (int, float)):
                if timestamp > 1e10:
                    timestamp = timestamp / 1000
                dt = datetime.fromtimestamp(timestamp)
            else:
                dt = timestamp
            
            now = datetime.now()
            diff = now - dt
            seconds = diff.total_seconds()
            
            if seconds < 60:
                return "just now"
            elif seconds < 3600:
                return f"{int(seconds/60)} minute{'s' if int(seconds/60) != 1 else ''} ago"
            elif seconds < 86400:
                return f"{int(seconds/3600)} hour{'s' if int(seconds/3600) != 1 else ''} ago"
            elif seconds < 604800:
                return f"{int(seconds/86400)} day{'s' if int(seconds/86400) != 1 else ''} ago"
            else:
                return f"{int(seconds/604800)} week{'s' if int(seconds/604800) != 1 else ''} ago"
        except Exception:
            return "Unknown"
    except Exception:
        return "Unknown"
