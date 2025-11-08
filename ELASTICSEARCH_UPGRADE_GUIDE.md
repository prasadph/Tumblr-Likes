# Elasticsearch Upgrade Guide

## Current Setup

- **Elasticsearch Server**: 6.6.0
- **Python Client**: 6.3.1
- **elasticsearch-dsl**: 6.4.0
- **Kibana**: 6.6.0

## Upgrade Options

### Option 1: Elasticsearch 7.x (Recommended Next Step)

**Why 7.x:**
- ✅ Still widely used and stable
- ✅ Good balance of features and stability
- ✅ Less breaking changes than 8.x
- ✅ Better Python 3.10 support

**Versions:**
- **Server**: 7.17.x (latest 7.x, LTS)
- **Python client**: 7.17.x
- **elasticsearch-dsl**: 7.4.x
- **Kibana**: 7.17.x

**Breaking Changes:**
- Removed `doc_type` (mapping types) - you'll need to update code
- Some API changes in queries
- Index mapping changes

### Option 2: Elasticsearch 8.x (Latest)

**Why 8.x:**
- ✅ Latest features and security
- ✅ Best Python 3.10 support
- ✅ Long-term support
- ⚠️ More breaking changes

**Versions:**
- **Server**: 8.11.x (latest stable)
- **Python client**: 8.11.x
- **elasticsearch-dsl**: 8.11.x
- **Kibana**: 8.11.x

**Breaking Changes:**
- Security enabled by default
- Removed `doc_type` (mapping types)
- API changes
- More strict validation

## Recommended Upgrade Path

### Phase 1: Upgrade to 7.17.x (Safest)

1. **Update docker-compose.yml:**
   ```yaml
   elasticsearch:
     image: docker.elastic.co/elasticsearch/elasticsearch:7.17.15
   
   kibana:
     image: docker.elastic.co/kibana/kibana:7.17.15
   ```

2. **Update requirements.txt:**
   ```
   elasticsearch==7.17.9
   elasticsearch-dsl==7.4.1
   ```

3. **Code Changes Needed:**
   - Remove `doc_type` parameter from all ES calls
   - Update index mappings (no more types)
   - Test all queries

### Phase 2: Later, Upgrade to 8.x (Optional)

After 7.x is stable, consider 8.x for latest features.

## Code Changes Required

### 1. Remove `doc_type` Parameter

**Current (6.x):**
```python
es.delete(id=post_id, doc_type=doc_type, index=index)
```

**New (7.x/8.x):**
```python
es.delete(id=post_id, index=index)  # doc_type removed
```

### 2. Update Index Mappings

**Current (6.x):**
```python
# Uses mapping types
```

**New (7.x/8.x):**
```python
# No mapping types - single `_doc` type
```

### 3. Update Search Queries

Some query syntax may need updates, but most should work.

## Migration Steps

1. **Backup your data** (critical!)
2. **Test in a separate environment first**
3. **Update docker-compose.yml**
4. **Update Python clients**
5. **Remove `doc_type` from code**
6. **Update index mappings**
7. **Test thoroughly**
8. **Migrate data** (if needed)

## Important Notes

⚠️ **Data Migration**: ES 6.x → 7.x requires data migration
⚠️ **Breaking Changes**: `doc_type` removal affects all ES operations
⚠️ **Downtime**: May require downtime for migration
⚠️ **Backup First**: Always backup before upgrading

## Recommendation

**Start with Elasticsearch 7.17.x** because:
- ✅ More stable than jumping to 8.x
- ✅ Still well-supported
- ✅ Easier migration path
- ✅ Good Python 3.10 support

Then later consider 8.x if you need latest features.

