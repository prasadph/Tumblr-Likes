from sync import update_likes


def index_likes():
    print("indexing Tumblr Likes")
    update_likes()
    print("Indexed Tumblr Likes to Elasticsearch")
