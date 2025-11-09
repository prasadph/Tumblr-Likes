# Elasticsearch 6.6.0 → 7.17.15 Migration Guide

## ✅ Changes Made

### 1. Docker Images Updated
- **Elasticsearch**: `6.6.0` → `7.17.15`
- **Kibana**: `6.6.0` → `7.17.15`

### 2. Python Clients Updated
- **elasticsearch**: `6.3.1` → `7.17.9`
- **elasticsearch-dsl**: `6.4.0` → `7.4.1`

### 3. Code Changes
- Removed `doc_type` parameter from:
  - `delete_like()` - `es.delete()`
  - `save_like()` - `es.index()`
  - `fetch_post()` - `es.get()`

## Migration Steps

### Step 1: Stop Current Services
```bash
docker compose down
```

### Step 2: Backup Data (Already Done ✅)
Your backup is in `./backups/`:
- `es_backup_tumblr_likes_1_*_mapping.json`
- `es_backup_tumblr_likes_1_*_settings.json`
- `es_backup_tumblr_likes_1_*_data.json`

### Step 3: Update Python Dependencies
```bash
# In Docker container
docker compose exec web pip install -r requirements.txt

# Or rebuild container
docker compose build web
```

### Step 4: Start New Elasticsearch 7.17.15
```bash
docker compose up -d elasticsearch
```

**Wait for ES to be ready** (check logs):
```bash
docker compose logs -f elasticsearch
# Look for: "started" message
```

### Step 5: Restore Data from Backup

**Option A: Using elasticdump (Recommended)**
```bash
# Restore mapping
elasticdump \
  --input=backups/es_backup_tumblr_likes_1_*_mapping.json \
  --output=http://localhost:9200/tumblr_likes_1 \
  --type=mapping

# Restore settings
elasticdump \
  --input=backups/es_backup_tumblr_likes_1_*_settings.json \
  --output=http://localhost:9200/tumblr_likes_1 \
  --type=settings

# Restore data (this will take time)
elasticdump \
  --input=backups/es_backup_tumblr_likes_1_*_data.json \
  --output=http://localhost:9200/tumblr_likes_1 \
  --type=data \
  --limit=1000 \
  --progress
```

**Option B: Re-index from scratch**
If you prefer to re-sync from Tumblr API:
```bash
docker compose exec web flask update-es
```

### Step 6: Verify Data
```bash
# Check index exists
curl http://localhost:9200/tumblr_likes_1

# Check document count
curl http://localhost:9200/tumblr_likes_1/_count

# Should show ~435,901 documents
```

### Step 7: Start All Services
```bash
docker compose up -d
```

### Step 8: Test Application
1. Open http://localhost:5000
2. Verify posts are loading
3. Test search functionality
4. Test tag filtering
5. Check Kibana at http://localhost:5601

## Important Notes

### Breaking Changes in ES 7.x

1. **No More Mapping Types**
   - ES 7.x removed `doc_type` (mapping types)
   - All documents use implicit `_doc` type
   - Code updated to remove `doc_type` parameter

2. **Index Compatibility**
   - ES 6.x indices are **not directly compatible** with ES 7.x
   - You **must restore from backup** or re-index
   - Old data volume won't work with new ES version

3. **Data Volume**
   - Old ES 6.x data in `esdata1` volume won't work
   - ES 7.x will create new index structure
   - You can delete old volume after verifying backup:
     ```bash
     docker volume rm tumblr_likes_esdata1
     ```

## Troubleshooting

### ES Won't Start
```bash
# Check logs
docker compose logs elasticsearch

# Common issues:
# - Memory limits (increase ES_JAVA_OPTS)
# - Permissions (check volume mounts)
```

### Data Not Restoring
```bash
# Check ES is ready
curl http://localhost:9200

# Check index exists
curl http://localhost:9200/_cat/indices

# Try re-running restore commands
```

### Application Errors
```bash
# Check web container logs
docker compose logs web

# Verify Python clients are updated
docker compose exec web pip list | grep elasticsearch
```

## Rollback Plan

If something goes wrong:

1. **Stop services**
   ```bash
   docker compose down
   ```

2. **Restore old docker-compose.yml**
   - Change ES back to `6.6.0`
   - Change Kibana back to `6.6.0`

3. **Restore old requirements.txt**
   - Change elasticsearch back to `6.3.1`
   - Change elasticsearch-dsl back to `6.4.0`

4. **Restore code** (revert doc_type changes)

5. **Start old version**
   ```bash
   docker compose up -d
   ```

6. **Restore data from backup** (if needed)

## Success Criteria

✅ Elasticsearch 7.17.15 running  
✅ Kibana 7.17.15 running  
✅ Index restored with ~435K documents  
✅ Application loads posts correctly  
✅ Search works  
✅ Tags work  
✅ Stats page works  

## Next Steps After Migration

1. Test all functionality thoroughly
2. Monitor for any errors
3. Consider upgrading to ES 8.x later (optional)
4. Update documentation

