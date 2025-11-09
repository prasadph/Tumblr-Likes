#!/bin/bash
# Reindex Elasticsearch data to fix liked_timestamp and timestamp as date types

set -e

ES_HOST="http://localhost:9200"
OLD_INDEX="tumblr_likes_1"
NEW_INDEX="tumblr_likes_2"

echo "=========================================="
echo "Reindexing to Fix Date Field Types"
echo "=========================================="
echo ""
echo "Old index: ${OLD_INDEX}"
echo "New index: ${NEW_INDEX}"
echo ""

# Step 1: Create new index with correct mapping
echo "Step 1: Creating new index with date mapping..."
curl -X PUT "${ES_HOST}/${NEW_INDEX}" \
  -H 'Content-Type: application/json' \
  -d @tumblr_mappings_es7.json

echo ""
echo "✓ New index created"

# Step 2: Reindex data
echo ""
echo "Step 2: Reindexing data (this may take a few minutes for ~96K documents)..."
curl -X POST "${ES_HOST}/_reindex?wait_for_completion=false" \
  -H 'Content-Type: application/json' \
  -d "{
    \"source\": {
      \"index\": \"${OLD_INDEX}\"
    },
    \"dest\": {
      \"index\": \"${NEW_INDEX}\"
    }
  }" | jq -r '.task // "Started"'

echo ""
echo "✓ Reindex started (check status with: curl ${ES_HOST}/_tasks?detailed=true&actions=*reindex)"
echo ""
echo "To check progress:"
echo "  curl ${ES_HOST}/${NEW_INDEX}/_count"
echo ""
echo "Once complete, update config.py: index = \"${NEW_INDEX}\""
