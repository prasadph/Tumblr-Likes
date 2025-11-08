#!/bin/bash
# Project-specific UV cache setup for external SSD
# Source this file when working on this project: source setup-uv-cache.sh

# Check if we're on the external drive
if [[ "$(df -P . | tail -1 | awk '{print $1}')" == *"/mnt/d"* ]] || [[ "$PWD" == "/mnt/d"* ]]; then
    export UV_CACHE_DIR="$(pwd)/.uv-cache"
    echo "✓ UV cache set to project directory (external SSD mode)"
else
    echo "✓ Using default UV cache location (laptop mode)"
fi
