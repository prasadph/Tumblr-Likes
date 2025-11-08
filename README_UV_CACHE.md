# UV Cache Configuration for External SSD

## Problem
When working on an external SSD, `uv` cache is on a different filesystem (`/home/.cache/uv`), causing hardlink failures and using more disk space.

## Solution (Project-Specific)

### Option 1: Use Setup Script (Recommended)

When working on the external drive, source the setup script:

```bash
source setup-uv-cache.sh
uv sync
```

This automatically detects if you're on the external drive and sets the cache accordingly.

### Option 2: Manual Setup (One-Time)

When working on external drive, set it for current session:

```bash
export UV_CACHE_DIR="$(pwd)/.uv-cache"
uv sync
```

### Option 3: Add to Shell Profile (Project-Specific)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Project-specific: Tumblr Likes on external SSD
if [[ "$PWD" == "/mnt/d/Prasad/tumblr-likes"* ]]; then
    export UV_CACHE_DIR="$PWD/.uv-cache"
fi
```

## Benefits

- ✅ **Saves disk space**: Enables hardlinking (same filesystem)
- ✅ **Removes warning**: No more hardlink warnings
- ✅ **Project-specific**: Only affects this project
- ✅ **Automatic**: Works on external drive, ignores on laptop

## Notes

- Cache directory `.uv-cache/` is gitignored
- On laptop, `uv` uses default cache location
- No global changes needed

