import pytumblr
import logging
from config import tumblr_config

logging.basicConfig(filename='logs/tumblr_index.log', level=logging.DEBUG)

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    *tumblr_config
)


def unlike(post_id, reblog_key):
    return client.unlike(post_id, reblog_key)


def like(post_id, reblog_key):
    return client.like(post_id, reblog_key)
