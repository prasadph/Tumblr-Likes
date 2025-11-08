#!/bin/bash
# Elasticsearch Backup Script using elasticdump
# This backs up your Elasticsearch index before upgrade

set -e

# Configuration
ES_HOST="http://localhost:9200"
INDEX_NAME="tumblr_likes_1"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PREFIX="${BACKUP_DIR}/es_backup_${INDEX_NAME}_${TIMESTAMP}"

echo "=========================================="
echo "Elasticsearch Backup Script"
echo "=========================================="
echo ""
echo "Index: ${INDEX_NAME}"
echo "Backup location: ${BACKUP_DIR}"
echo "Timestamp: ${TIMESTAMP}"
echo ""

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Check if elasticdump is available
if command -v elasticdump &> /dev/null; then
    ELASTICDUMP_CMD="elasticdump"
    echo "Using local elasticdump installation"
elif docker ps | grep -q elasticsearch; then
    # Use elasticdump via Docker
    ELASTICDUMP_CMD="docker run --rm --network tumblr_likes_default -v $(pwd)/backups:/backups taskrabbit/elasticsearch-dump"
    ES_HOST="http://elasticsearch:9200"
    echo "Using elasticdump via Docker"
else
    echo "Error: elasticdump not found and Docker not available"
    echo "Install elasticdump: npm install -g elasticdump"
    exit 1
fi

echo ""
echo "Step 1: Backing up index mapping..."
if command -v elasticdump &> /dev/null; then
    elasticdump \
        --input="${ES_HOST}/${INDEX_NAME}" \
        --output="${BACKUP_PREFIX}_mapping.json" \
        --type=mapping
else
    docker run --rm --network tumblr_likes_default \
        -v "$(pwd)/backups:/backups" \
        taskrabbit/elasticsearch-dump \
        --input="${ES_HOST}/${INDEX_NAME}" \
        --output="/backups/es_backup_${INDEX_NAME}_${TIMESTAMP}_mapping.json" \
        --type=mapping
fi

echo "✓ Mapping backed up"

echo ""
echo "Step 2: Backing up index settings..."
if command -v elasticdump &> /dev/null; then
    elasticdump \
        --input="${ES_HOST}/${INDEX_NAME}" \
        --output="${BACKUP_PREFIX}_settings.json" \
        --type=settings
else
    docker run --rm --network tumblr_likes_default \
        -v "$(pwd)/backups:/backups" \
        taskrabbit/elasticsearch-dump \
        --input="${ES_HOST}/${INDEX_NAME}" \
        --output="/backups/es_backup_${INDEX_NAME}_${TIMESTAMP}_settings.json" \
        --type=settings
fi

echo "✓ Settings backed up"

echo ""
echo "Step 3: Backing up index data (this may take a while for large indices)..."
echo "  Index size: ~551MB, ~435K documents"
if command -v elasticdump &> /dev/null; then
    elasticdump \
        --input="${ES_HOST}/${INDEX_NAME}" \
        --output="${BACKUP_PREFIX}_data.json" \
        --type=data \
        --limit=1000 \
        --progress
else
    docker run --rm --network tumblr_likes_default \
        -v "$(pwd)/backups:/backups" \
        taskrabbit/elasticsearch-dump \
        --input="${ES_HOST}/${INDEX_NAME}" \
        --output="/backups/es_backup_${INDEX_NAME}_${TIMESTAMP}_data.json" \
        --type=data \
        --limit=1000
fi

echo "✓ Data backed up"

echo ""
echo "=========================================="
echo "Backup Complete!"
echo "=========================================="
echo ""
echo "Backup files:"
ls -lh "${BACKUP_DIR}/es_backup_${INDEX_NAME}_${TIMESTAMP}"* 2>/dev/null || echo "Files created in ${BACKUP_DIR}/"
echo ""
echo "File sizes:"
du -h "${BACKUP_DIR}/es_backup_${INDEX_NAME}_${TIMESTAMP}"* 2>/dev/null | tail -3 || echo "Calculating..."
echo ""
echo "✅ Backup saved to: ${BACKUP_DIR}/"
echo ""

