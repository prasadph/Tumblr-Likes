# Elasticsearch 7.17.15 Upgrade - Complete ✅

## Summary

Successfully upgraded from Elasticsearch 6.6.0 to 7.17.15 with all compatibility fixes applied.

## What Was Upgraded

### Docker Images
- **Elasticsearch**: `6.6.0` → `7.17.15`
- **Kibana**: `6.6.0` → `7.17.15`

### Python Clients
- **elasticsearch**: `6.3.1` → `7.17.9`
- **elasticsearch-dsl**: `6.4.0` → `7.4.1`

## Code Changes Made

### 1. Removed `doc_type` Parameter (ES 7.x Requirement)
- **File**: `core/elasticsearch/elastic.py`
- **Functions updated**:
  - `delete_like()` - removed `doc_type`
  - `save_like()` - removed `doc_type`
  - `fetch_post()` - removed `doc_type`
- **Note**: ES 7.x doesn't support mapping types - all documents use implicit `_doc` type

### 2. Fixed ES 7.x `hits.total` Format
- **File**: `views/likes.py`
- **Change**: Access `hits.total.value` instead of `hits.total` (ES 7.x uses object, not number)
- **Impact**: Fixed likes page and stats page showing correct counts

### 3. Added `track_total_hits=True` for Accurate Counts
- **Files**: 
  - `core/elasticsearch/elastic.py` - `get_search_result()`
  - `views/likes.py` - `stats()` function
  - `get_html_posts_images.py` - count query
- **Why**: ES 7.x defaults to tracking only 10,000 hits. This ensures accurate counts for all queries.

### 4. Fixed Empty Search String Handling
- **File**: `core/elasticsearch/elastic.py`
- **Functions**: `get_search_result()`, `get_timestamp_range()`, `get_top_tags_for_search()`
- **Change**: Only apply `MultiMatch` filter if search string is not empty
- **Why**: Empty search string with MultiMatch was causing queries to fail

### 5. Fixed `sync.py` Offset Calculation Bug
- **File**: `sync.py`
- **Change**: `offset = int(offset) // 1000 - 1` → `offset = int(offset) - 1`
- **Why**: `liked_timestamp` is in seconds, not milliseconds. Dividing by 1000 was always wrong.
- **Impact**: Sync now correctly starts from latest post instead of 1970

### 6. Prevented Overwriting Existing Posts
- **File**: `core/elasticsearch/elastic.py` - `save_like()`
- **Change**: Use `op_type='create'` with proper exception handling
- **Why**: Preserves original posts with original images (before they got banned/replaced)
- **Impact**: Existing posts are skipped, only new posts are added

### 7. Added Discovery Type for Single-Node
- **File**: `docker-compose.yml`
- **Change**: Added `discovery.type=single-node`
- **Why**: ES 7.x requires discovery settings for single-node clusters

## Migration Steps Completed

1. ✅ Created backup using elasticdump (96,794 documents)
2. ✅ Stopped ES 6.6.0 services
3. ✅ Started ES 7.17.15 with single-node discovery
4. ✅ Restored data from backup (auto-creates ES 7.x compatible index)
5. ✅ Updated Python dependencies
6. ✅ Fixed all compatibility issues
7. ✅ Tested and verified functionality

## Current Status

- ✅ Elasticsearch 7.17.15: **Online**
- ✅ Kibana 7.17.15: **Online**
- ✅ Web Application: **Running**
- ✅ Index: **tumblr_likes_1** (96,794 documents)
- ✅ All compatibility fixes: **Applied**

## Testing Checklist

- [x] Elasticsearch responds correctly
- [x] Index has correct document count (96,794)
- [x] Likes page loads and shows posts
- [x] Stats page shows correct count (96,794)
- [x] Search functionality works
- [x] Tag filtering works
- [x] Sync script works (skips existing posts)
- [x] No errors in logs

## Files Modified

1. `docker-compose.yml` - Updated ES and Kibana versions, added discovery.type
2. `requirements.txt` - Updated elasticsearch and elasticsearch-dsl versions
3. `pyproject.toml` - Updated elasticsearch and elasticsearch-dsl versions
4. `core/elasticsearch/elastic.py` - Removed doc_type, fixed queries, added track_total_hits
5. `views/likes.py` - Fixed hits.total access, added track_total_hits
6. `get_html_posts_images.py` - Added track_total_hits
7. `sync.py` - Fixed offset calculation bug
8. `SYNC_GUIDELINES.md` - Updated documentation

## Breaking Changes Handled

1. **Mapping Types Removed**: ES 7.x doesn't support `doc_type` - removed from all code
2. **hits.total Format**: Changed from number to object with `.value` property
3. **Default Hit Tracking**: ES 7.x defaults to 10,000 - added `track_total_hits=True`
4. **Discovery Settings**: ES 7.x requires discovery config for single-node

## Next Steps (Optional)

1. Consider upgrading to ES 8.x in the future (more breaking changes)
2. Enable Elasticsearch security features (currently disabled)
3. Monitor performance and adjust as needed

## Notes

- Backup is preserved in `./backups/` directory
- Original posts with original images are preserved
- `save_like()` now prevents overwriting existing posts
- All ES 7.x compatibility issues have been resolved

---

**Upgrade Date**: November 9, 2025  
**Status**: ✅ Complete and Verified

