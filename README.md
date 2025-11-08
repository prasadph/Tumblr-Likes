# Tumblr Likes with ElasticSearch and Flask

> **📖 For comprehensive documentation, see [README_NEW.md](README_NEW.md)**

## Quick Start

- `pip install -r requirements.txt`

- `cat config.py.sample > config.py`

- Install Elasticsearch 6.4 or higher
- Create index with mappings and given in tumblr_mappings.json
- Add Tumblr API credentials and other info in config.py
- `flask update-es` to load your liked posts in Elasticsearch and images to location as defined in config
- `FLASK=app.py;export FLASK_ENV=development;flask run`

---

**For detailed setup instructions, features, API documentation, and troubleshooting, please see [README_NEW.md](README_NEW.md)**
