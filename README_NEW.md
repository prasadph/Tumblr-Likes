# Tumblr Likes Browser

A Flask-based web application for browsing, searching, and managing your Tumblr liked posts. The application uses Elasticsearch for powerful search capabilities and stores images locally for offline access.

## 🎯 Features

- **Browse Liked Posts**: Paginated view of all your Tumblr likes
- **Full-Text Search**: Search through post content, tags, and summaries using Elasticsearch
- **Filter by Blog**: Filter posts by specific Tumblr blogs
- **Filter by Tags**: View posts filtered by tags
- **Individual Post View**: Detailed view of each liked post
- **Image Management**: Automatic download and local storage of images
- **Like/Unlike Actions**: Unlike or relike posts directly from the web interface
- **Docker Support**: Easy deployment with Docker Compose

## 🏗️ Architecture

### Tech Stack
- **Backend**: Flask 1.0.2
- **Search Engine**: Elasticsearch 6.3.1
- **API Client**: PyTumblr 0.0.8
- **Frontend**: Jinja2 templates
- **Task Queue**: RQ (Redis Queue) for background jobs

### Components
- **Flask Web Application**: Main web interface and API endpoints
- **Elasticsearch Integration**: Indexing and search functionality
- **Tumblr API Sync**: Fetches and syncs liked posts from Tumblr
- **Image Downloader**: Downloads and serves images locally
- **Maintenance Scripts**: Utilities for data cleanup and management

## 📋 Prerequisites

- Python 3.6+
- Elasticsearch 6.4 or higher
- Tumblr API credentials (Consumer Key, Consumer Secret, OAuth Token, OAuth Secret)
- Docker and Docker Compose (optional, for containerized deployment)

## 🚀 Installation

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Tumblr_Likes
   ```

2. **Configure the application**
   ```bash
   cp config.py.sample config.py
   # Edit config.py with your Tumblr API credentials and settings
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - Elasticsearch on port 9200
   - Flask web application on port 5000
   - Kibana on port 5601 (optional, for Elasticsearch management)
   - Dejavu on port 1358 (optional, Elasticsearch browser)

4. **Create Elasticsearch index**
   ```bash
   docker-compose exec web flask create-index
   ```

5. **Sync your Tumblr likes**
   ```bash
   docker-compose exec web flask update-es
   ```

6. **Access the application**
   - Web interface: http://localhost:5000
   - Elasticsearch: http://localhost:9200
   - Kibana: http://localhost:5601
   - Dejavu: http://localhost:1358

### Option 2: Manual Installation

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install and start Elasticsearch**
   - Download Elasticsearch 6.4+ from [elastic.co](https://www.elastic.co/downloads/elasticsearch)
   - Start Elasticsearch service
   - Verify it's running: `curl http://localhost:9200`

3. **Configure the application**
   ```bash
   cp config.py.sample config.py
   # Edit config.py with your settings
   ```

4. **Create Elasticsearch index**
   ```bash
   export FLASK_APP=app.py
   flask create-index
   ```

5. **Sync your Tumblr likes**
   ```bash
   flask update-es
   ```

6. **Run the Flask application**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run
   # Or: python app.py
   ```

## ⚙️ Configuration

Edit `config.py` with your settings:

```python
# Tumblr API OAuth credentials (4-tuple)
tumblr_config = (
    'YOUR_CONSUMER_KEY',
    'YOUR_CONSUMER_SECRET',
    'YOUR_OAUTH_TOKEN',
    'YOUR_OAUTH_SECRET'
)

# Local image storage directory
image_repo = "/media/"

# Elasticsearch settings
index = "tumblr_likes_1"
doc_type = "doc"
host = "elasticsearch"  # Use "localhost" for manual installation

# Application settings
logs_path = "logs/tumblr.log"
posts_per_page = 40
```

### Getting Tumblr API Credentials

1. Go to [Tumblr API Applications](https://www.tumblr.com/oauth/apps)
2. Register a new application
3. Get your OAuth credentials (Consumer Key, Consumer Secret)
4. Generate OAuth Token and Secret for your account

## 📖 Usage

### Web Interface

- **Browse Likes**: Navigate to `http://localhost:5000/likes`
- **Search**: Use the search box to find posts by content
- **Filter by Blog**: Select a blog from the dropdown
- **Filter by Tag**: Click on tags to filter posts
- **View Post**: Click on any post to see details
- **Unlike/Relike**: Use the API endpoints or add UI buttons

### CLI Commands

```bash
# Update Elasticsearch index with latest likes
flask update-es

# Create Elasticsearch index with mappings
flask create-index
```

### API Endpoints

- `GET /likes` - Browse liked posts (supports query parameters: `search`, `blog_name`, `tag`, `offset`, `timestamp`)
- `GET /post/<code>` - View individual post details
- `GET /photos/<code>` - Serve locally stored images
- `POST /api/unlike` - Unlike a post (requires JSON: `{"id": "...", "reblog_key": "..."}`)
- `POST /api/relike` - Relike a post (requires JSON: `{"id": "...", "reblog_key": "..."}`)
- `GET /test` - Health check endpoint

## 📁 Project Structure

```
Tumblr_Likes/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration file (create from config.py.sample)
├── sync.py                     # Main sync script for fetching Tumblr likes
├── tasks.py                    # Task queue wrapper for background jobs
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── tumblr_mappings.json        # Elasticsearch index mappings
│
├── core/                       # Core application modules
│   ├── elasticsearch/
│   │   ├── es.py              # Elasticsearch connection management
│   │   ├── elastic.py         # Elasticsearch CRUD operations
│   │   └── post.py            # Elasticsearch DSL document model
│   └── tumblr/
│       └── likes.py           # Tumblr API wrapper
│
├── views/                      # Flask view handlers
│   └── likes.py               # Main web interface routes
│
├── templates/                  # Jinja2 HTML templates
│   └── likes/                 # Template files
│
├── static/                     # Static assets (CSS, JS, images)
│
├── logs/                       # Application logs
│
├── extra/                      # Legacy/experimental code
│   └── tumblr.py              # Old sync script
│
└── scripts/                      # Maintenance and utility scripts
    ├── get_html_posts_images.py  # Extract images from HTML posts
    ├── missing_images.py         # Find missing image files
    ├── delete_images.py          # Clean up orphaned images
    ├── backup_elasticsearch.sh   # Backup Elasticsearch data
    └── reindex_with_date_mapping.sh  # Reindex with date mappings
```

## 🔧 Maintenance Scripts

### Extract Images from HTML Posts
```bash
python scripts/get_html_posts_images.py
```
Finds text posts with embedded images and downloads missing images.

### Find Missing Images
```bash
python scripts/missing_images.py
```
Scans all posts and reports which referenced images are missing locally.

### Clean Up Orphaned Images
```bash
python scripts/delete_images.py
```
Finds images in the directory that aren't referenced in any post and moves them to an "extra" folder.

## 🐛 Troubleshooting

### Elasticsearch Connection Issues
- Verify Elasticsearch is running: `curl http://localhost:9200`
- Check `host` setting in `config.py` (use `"localhost"` for manual install, `"elasticsearch"` for Docker)
- Ensure Elasticsearch version is 6.4+ (app uses Elasticsearch 6.3.1 client)

### Image Download Issues
- Check `image_repo` path in `config.py` exists and is writable
- Verify disk space is available
- Check network connectivity for image downloads

### Tumblr API Rate Limits
- The sync script includes 3-second delays between requests
- If you hit rate limits, increase the delay in `sync.py`

### Index Creation Fails
- Ensure Elasticsearch is running before creating index
- Check `tumblr_mappings.json` file exists and is valid JSON
- Verify index name in `config.py` doesn't conflict with existing indices

## 📝 Notes

- **Legacy Application**: This is a legacy application using older versions of dependencies
- **Security**: API credentials are stored in `config.py` - keep this file secure and never commit it
- **Data Storage**: Images are stored locally - ensure sufficient disk space
- **Elasticsearch Version**: The app is designed for Elasticsearch 6.x - newer versions may have compatibility issues

## 🔄 Data Sync Process

1. Fetches liked posts from Tumblr API (50 posts per request)
2. Downloads images to local storage (`/media/` by default)
3. Indexes posts in Elasticsearch with metadata
4. Uses `liked_timestamp` for pagination and incremental updates
5. Processes photos, videos, and other post types

## 📄 License

See [LICENSE.md](LICENSE.md) for details.

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

---

**Note**: For the original quick-start guide, see [README.md](README.md).

