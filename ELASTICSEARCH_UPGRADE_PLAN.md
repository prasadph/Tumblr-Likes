# Elasticsearch Upgrade Plan

## Current State
- **Server**: 6.6.0
- **Python Client**: 6.3.1
- **elasticsearch-dsl**: 6.4.0
- **Kibana**: 6.6.0

## Recommended Upgrade Path

### Option 1: Elasticsearch 7.17.x (Recommended - Safer)

**Why 7.17.x:**
- ✅ Latest 7.x LTS (Long Term Support)
- ✅ Stable and well-tested
- ✅ Good Python 3.10 support
- ✅ Less breaking changes than 8.x
- ✅ Still widely used in production

**Target Versions:**
- **Server**: `7.17.15` (latest 7.x)
- **Python client**: `7.17.9`
- **elasticsearch-dsl**: `7.4.1`
- **Kibana**: `7.17.15`

**Breaking Changes:**
- ❌ `doc_type` removed (used in 3 places in your code)
- ⚠️ Some query syntax changes (minimal for your usage)
- ⚠️ Index mapping changes (no more types)

### Option 2: Elasticsearch 8.11.x (Latest - More Changes)

**Why 8.11.x:**
- ✅ Latest features and security
- ✅ Best Python 3.10 support
- ✅ Long-term support
- ⚠️ More breaking changes
- ⚠️ Security enabled by default

**Target Versions:**
- **Server**: `8.11.0` (latest stable)
- **Python client**: `8.11.0`
- **elasticsearch-dsl**: `8.11.0`
- **Kibana**: `8.11.0`

**Breaking Changes:**
- ❌ `doc_type` removed
- ❌ Security enabled by default (may need config)
- ⚠️ More API changes
- ⚠️ Stricter validation

## Code Changes Required

### Files to Update:

1. **`core/elasticsearch/elastic.py`** (3 places):
   ```python
   # Current (6.x):
   es.delete(id=post_id, doc_type=doc_type, index=index)
   es.index(index=index, doc_type=doc_type, id=like["id"], body=like)
   es.get(index=index, doc_type=doc_type, id=code)
   
   # New (7.x/8.x):
   es.delete(id=post_id, index=index)
   es.index(index=index, id=like["id"], body=like)
   es.get(index=index, id=code)
   ```

2. **`config.py`**:
   - Can remove `doc_type` variable (or keep for backward compat)

3. **Index mappings**:
   - May need to recreate index without types

## Migration Steps

### For ES 7.17.x:

1. **Backup data** (critical!)
   ```bash
   # Export your data
   docker compose exec elasticsearch curl -X GET "localhost:9200/_all/_search?pretty" > backup.json
   ```

2. **Update docker-compose.yml:**
   ```yaml
   elasticsearch:
     image: docker.elastic.co/elasticsearch/elasticsearch:7.17.15
   
   kibana:
     image: docker.elastic.co/kibana/kibana:7.17.15
   ```

3. **Update requirements.txt:**
   ```
   elasticsearch==7.17.9
   elasticsearch-dsl==7.4.1
   ```

4. **Update code** (remove `doc_type`)

5. **Recreate index** (if needed)

6. **Test thoroughly**

## Recommendation

**Start with Elasticsearch 7.17.15** because:
- ✅ Safer migration path
- ✅ Still well-supported
- ✅ Good balance of features/stability
- ✅ Easier to test and validate

Then later consider 8.x if you need latest features.

## Quick Start: ES 7.17.x

I can help you:
1. Update docker-compose.yml
2. Update requirements.txt
3. Remove `doc_type` from code
4. Test the migration

Would you like me to proceed with ES 7.17.x upgrade?

