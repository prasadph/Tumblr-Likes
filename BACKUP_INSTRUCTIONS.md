# Elasticsearch Backup Instructions

## Quick Backup

Run the backup script:
```bash
./backup_elasticsearch.sh
```

Or manually:

### 1. Backup Mapping
```bash
elasticdump \
  --input=http://localhost:9200/tumblr_likes_1 \
  --output=backups/backup_mapping.json \
  --type=mapping
```

### 2. Backup Settings
```bash
elasticdump \
  --input=http://localhost:9200/tumblr_likes_1 \
  --output=backups/backup_settings.json \
  --type=settings
```

### 3. Backup Data (takes time for large indices)
```bash
elasticdump \
  --input=http://localhost:9200/tumblr_likes_1 \
  --output=backups/backup_data.json \
  --type=data \
  --limit=1000 \
  --progress
```

## Using Docker (if elasticdump not installed)

```bash
# Mapping
docker run --rm --network tumblr_likes_default \
  -v $(pwd)/backups:/backups \
  taskrabbit/elasticsearch-dump \
  --input=http://elasticsearch:9200/tumblr_likes_1 \
  --output=/backups/backup_mapping.json \
  --type=mapping

# Settings
docker run --rm --network tumblr_likes_default \
  -v $(pwd)/backups:/backups \
  taskrabbit/elasticsearch-dump \
  --input=http://elasticsearch:9200/tumblr_likes_1 \
  --output=/backups/backup_settings.json \
  --type=settings

# Data
docker run --rm --network tumblr_likes_default \
  -v $(pwd)/backups:/backups \
  taskrabbit/elasticsearch-dump \
  --input=http://elasticsearch:9200/tumblr_likes_1 \
  --output=/backups/backup_data.json \
  --type=data \
  --limit=1000
```

## Restore from Backup

After upgrade, restore with:

```bash
# Restore mapping
elasticdump \
  --input=backups/backup_mapping.json \
  --output=http://localhost:9200/tumblr_likes_1 \
  --type=mapping

# Restore settings
elasticdump \
  --input=backups/backup_settings.json \
  --output=http://localhost:9200/tumblr_likes_1 \
  --type=settings

# Restore data
elasticdump \
  --input=backups/backup_data.json \
  --output=http://localhost:9200/tumblr_likes_1 \
  --type=data \
  --limit=1000
```

## Backup Size Estimate

- **Index**: tumblr_likes_1
- **Documents**: ~435,901
- **Size**: ~551MB
- **Estimated backup time**: 5-15 minutes (depending on system)

## Verify Backup

```bash
# Check backup files exist
ls -lh backups/

# Verify JSON is valid
jq . backups/backup_mapping.json > /dev/null && echo "Mapping OK"
jq . backups/backup_settings.json > /dev/null && echo "Settings OK"
head -1 backups/backup_data.json | jq . > /dev/null && echo "Data OK"
```

## Notes

- Backups are saved to `./backups/` directory
- Each backup includes a timestamp
- Keep backups safe - they're your safety net for upgrades!
- Consider compressing large backups: `gzip backups/backup_data.json`

