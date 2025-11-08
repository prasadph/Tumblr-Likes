# Syncing Guidelines

## Overview

The sync process fetches your liked posts from Tumblr API and indexes them in Elasticsearch, while also downloading images locally.

## How Syncing Works

### Incremental Sync (Default Behavior)

When you run `flask update-es` or `python sync.py`, the system:

1. **Finds the latest post** in Elasticsearch using `get_max_elastic_id()`
   - Gets the maximum `liked_timestamp` from your existing indexed posts
   - Converts it to the offset format: `timestamp // 1000 - 1`

2. **Fetches new posts** from Tumblr API
   - Starts from the timestamp of your most recent indexed post
   - Fetches 50 posts per request (Tumblr API maximum)
   - Uses `after` parameter for pagination

3. **Processes each post**:
   - Downloads images from photo posts to `image_repo` directory
   - Indexes the post in Elasticsearch (uses post `id` as document ID)
   - If a post already exists (same ID), it will be **updated** (not duplicated)

4. **Continues until no more posts**
   - Stops when API returns fewer than 50 posts
   - Stops when API returns 0 posts

### Key Behaviors

- **Idempotent**: Running sync multiple times is safe
  - Posts with the same ID will be updated, not duplicated
  - Images are only downloaded if they don't exist locally

- **Incremental**: Only fetches posts newer than what's already indexed
  - First run: Fetches all your likes (can take a long time!)
  - Subsequent runs: Only fetches new likes since last sync

- **Rate Limiting**: 3-second delay between API requests
  - Prevents hitting Tumblr API rate limits
  - Can be adjusted in `sync.py` line 39 if needed

## When to Run Sync

### Recommended Schedule

- **Initial Setup**: Run once to index all existing likes
- **Regular Updates**: Run daily/weekly to catch new likes
- **After Unliking**: Not necessary (unlike operations update Elasticsearch directly)
- **After Long Gaps**: Run if you haven't synced in a while

### Running Sync

**Option 1: Using Flask CLI (Recommended)**
```bash
flask update-es
```

**Option 2: Direct Python Script**
```bash
python sync.py
```

**Option 3: Using Docker**
```bash
docker-compose exec web flask update-es
```

**Option 4: Background Task (if using RQ)**
```python
from tasks import index_likes
index_likes()  # Can be queued with RQ
```

### ⚠️ Important: Download HTML Post Images

After running the main sync, you should also run `get_html_posts_images.py` to download images embedded in text/HTML posts:

```bash
python get_html_posts_images.py
```

**Why?** The main sync only downloads images from photo posts. Text posts with embedded images in their HTML body are not processed. This script:
- Finds all text posts (excluding photo/video/link/answer types)
- Parses HTML to extract `<img>` tags
- Downloads those images to your `image_repo` directory
- Handles both Tumblr-hosted and external images (with hashing for external URLs)

**When to run:**
- After initial sync
- Periodically to catch new text posts with images
- If you notice missing images in text posts

## What Gets Synced

### ✅ Synced Items

- **Post Metadata**: All post fields (id, tags, blog_name, summary, etc.)
- **Photo Posts**: Images are downloaded to `image_repo` directory
- **Text Posts**: Content and metadata
- **Post Timestamps**: `liked_timestamp` for sorting/filtering

### ⚠️ Partially Synced

- **Video Posts**: Metadata is synced, but videos are NOT downloaded
  - See line 65 in `sync.py`: `# write code to process videos and other types`
  - Videos would need additional implementation

- **HTML Post Images**: Images embedded in text posts are NOT automatically downloaded
  - Use `get_html_posts_images.py` script separately to backfill these

### ❌ Not Synced

- **Video Files**: Video URLs are stored but files aren't downloaded
- **External Images**: Images from non-Tumblr domains in HTML posts
- **Deleted Posts**: If you unlike a post, it's removed from Elasticsearch but sync won't re-add it

## Sync Process Details

### Step-by-Step Flow

```
1. Get max liked_timestamp from Elasticsearch
   ↓
2. Calculate offset: (max_timestamp // 1000) - 1
   ↓
3. Fetch 50 posts from Tumblr API (after=offset)
   ↓
4. For each post:
   - Download images (if photo post and image doesn't exist)
   - Index/update in Elasticsearch
   ↓
5. Update offset to last post's timestamp - 1
   ↓
6. Repeat from step 3 until < 50 posts returned
```

### Logging

- **Log File**: `logs/tumblr_index.log`
- **Logs**: Each post indexing result, API timestamps, download status
- **Console Output**: Progress updates, post summaries, final count

## Troubleshooting Sync Issues

### Sync Stops Early

**Problem**: Sync completes but you know there are more likes

**Solutions**:
- Check if you hit Tumblr API rate limits (wait and retry)
- Verify Elasticsearch is running and accessible
- Check `logs/tumblr_index.log` for errors
- Ensure `get_max_elastic_id()` is returning correct timestamp

### Missing Images

**Problem**: Posts are indexed but images aren't downloaded

**Solutions**:
- Check `image_repo` path in `config.py` exists and is writable
- Verify disk space is available
- Check network connectivity
- Run `missing_images.py` to find missing images
- Run `get_html_posts_images.py` for HTML post images

### Duplicate Posts

**Problem**: Same post appears multiple times

**Note**: This shouldn't happen - posts use `id` as document ID, so duplicates are updated, not created.

**If it happens**:
- Check if post IDs are consistent
- Verify Elasticsearch index mapping
- Check for index corruption

### Rate Limiting

**Problem**: Getting rate limited by Tumblr API

**Solutions**:
- Increase delay in `sync.py` line 39 (currently 3 seconds)
- Run sync during off-peak hours
- Check Tumblr API status page
- Verify your API credentials are valid

### Sync Takes Too Long

**First sync** can take hours if you have thousands of likes:
- 50 posts per request
- 3 seconds between requests
- Example: 10,000 likes = ~200 requests = ~10 minutes minimum (plus download time)

**Solutions**:
- Let it run in background
- Use `tasks.py` with RQ for background processing
- Consider running overnight for initial sync

## Best Practices

1. **Regular Syncs**: Run sync regularly (daily/weekly) rather than letting it accumulate
2. **Complete Image Sync**: Always run both:
   - `flask update-es` (or `python sync.py`) - for photo post images
   - `python get_html_posts_images.py` - for HTML/text post images
3. **Monitor Logs**: Check `logs/tumblr_index.log` for issues
4. **Disk Space**: Ensure `image_repo` has sufficient space for images
5. **Backup**: Consider backing up Elasticsearch data periodically
6. **Verify**: After sync, check web interface to verify new posts appear
7. **HTML Images**: Run `get_html_posts_images.py` after each sync to ensure all images are downloaded

## Advanced: Full Re-sync

If you need to re-sync everything from scratch:

1. **Delete Elasticsearch index**:
   ```bash
   # Via curl
   curl -X DELETE "localhost:9200/tumblr_likes_1"
   
   # Or recreate via Flask
   flask create-index
   ```

2. **Clear image directory** (optional, if you want fresh downloads):
   ```bash
   # Backup first!
   rm -rf /media/*
   ```

3. **Run sync**:
   ```bash
   flask update-es
   python get_html_posts_images.py  # Don't forget HTML post images!
   ```

## Monitoring Sync Progress

### Check Current Status

```bash
# Count indexed posts
curl "localhost:9200/tumblr_likes_1/_count"

# Get latest timestamp
curl "localhost:9200/tumblr_likes_1/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "max_timestamp": {
      "max": { "field": "liked_timestamp" }
    }
  }
}'
```

### View Logs

```bash
# Watch log file in real-time
tail -f logs/tumblr_index.log

# Check for errors
grep -i error logs/tumblr_index.log
```

## Notes

- **Post IDs are unique**: Elasticsearch uses post `id` as document ID, preventing duplicates
- **Images are cached**: Images are only downloaded if they don't exist locally
- **Sync is one-way**: Changes in Elasticsearch don't sync back to Tumblr
- **Unliking**: When you unlike via the web interface, the post is deleted from Elasticsearch immediately (no need to re-sync)

