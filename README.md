# Tumblr Likes with ElasticSearch and Flask

## Use this to browse and search through your Tumblr Likes
- `pip install -r requirements.txt`

- `cat config.py.example > config.py`

- Install Elasticsearch 6.4 or higher
- Create index with mappings and given in tumblr_mappings.json
- Add Tumblr API credentials and other info in config.py
- `flask update-es` to load your liked posts in Elasticsearch and images to location as defined in config
- `FLASK=app.py;export FLASK_ENV=development;flask run`

