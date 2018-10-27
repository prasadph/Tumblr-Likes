import pytumblr
import logging
from config import tumblr_config
from core.elasticsearch.elastic import delete_like

logging.basicConfig(filename='logs/tumblr_index.log', level=logging.DEBUG)

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    *tumblr_config
)


def unlike(post_id, reblog_key):
    tumblr_response = client.unlike(post_id, reblog_key)
    if not tumblr_response:
        tumblr_response = "success"

    elastic_response = delete_like(post_id)
    return {'tumblr': tumblr_response, "elastic": elastic_response}


def like(post_id, reblog_key):
    tumblr_response = client.like(post_id, reblog_key)
    if not tumblr_response:
        tumblr_response = "success"
    return {'tumblr': tumblr_response, "elastic": []}
