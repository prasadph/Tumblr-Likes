# Code Review: get_html_posts_images.py

## 🔴 Critical Issues (Must Fix Before Running)

### 1. **Logic Bug: External Image Filename Not Used** (Lines 80-84)
```python
if "media.tumblr.com" not in src: 
    m = hashlib.shake_128(str.encode(src)).hexdigest(5)
    filename = image_repo + str(m)+"-" +src.rsplit('/', 1)[1]
    pass  # ❌ This does nothing!
```
**Problem**: The code creates a hashed filename for external images but then has `pass`, so it continues to line 86 which uses the **original filename** (line 78), not the hashed one. External images will fail to save correctly.

**Fix**: Remove `pass` or restructure the logic:
```python
if "media.tumblr.com" not in src: 
    m = hashlib.shake_128(str.encode(src)).hexdigest(5)
    filename = image_repo + str(m) + "-" + src.rsplit('/', 1)[1]
else:
    filename = image_repo + src.rsplit('/', 1)[1]
```

### 2. **Directory Not Writable**
**Problem**: `/media/` directory exists but is **not writable** by your user.
- Script will crash when trying to save images
- Error: `PermissionError: [Errno 13] Permission denied`

**Fix Options**:
- Change `image_repo` in `config.py` to a writable directory
- Fix permissions: `sudo chmod 777 /media/` (or better: `sudo chown $USER:$USER /media/`)
- Use a different path like `./images/` or `~/tumblr_images/`

### 3. **No Error Handling**
**Problem**: If `save_image()` fails (network error, disk full, permission denied), the script will crash.

**Issues**:
- No try/except around `save_image()` call (line 88)
- `save_image()` in `sync.py` also has no error handling
- Network timeouts, 404 errors, etc. will crash the script

**Fix**: Add error handling:
```python
try:
    if not os.path.isfile(filename):
        print(src, filename)
        save_image(src, filename)
except Exception as e:
    print(f"Error downloading {src}: {e}")
    continue
```

## ⚠️ Major Issues (Should Fix)

### 4. **No Pagination - Only Processes 10,000 Posts**
**Problem**: Query has `"size":10000` (line 61). If you have more than 10,000 text posts, the rest won't be processed.

**Fix**: Use Elasticsearch scroll API or pagination:
```python
resp = es.search(index=index, body=query, scroll='10m', size=1000)
scroll_id = resp['_scroll_id']
while len(resp['hits']['hits']) > 0:
    # process posts
    resp = es.scroll(scroll_id=scroll_id, scroll='10m')
```

### 5. **No Rate Limiting**
**Problem**: Unlike `sync.py` which has `time.sleep(3)`, this script has **no delays** between downloads. Will likely hit:
- Network rate limits
- Tumblr rate limits (if downloading from Tumblr)
- Server rate limits

**Fix**: Add delay between downloads:
```python
import time
# After line 88
time.sleep(1)  # or 2-3 seconds for external sites
```

### 6. **No Input Validation**
**Problem**: Doesn't check if `src` is None or empty before processing.

**Fix**:
```python
src = image.get("src")
if not src or not src.strip():
    continue
```

### 7. **No Directory Existence Check**
**Problem**: Doesn't verify `image_repo` directory exists before trying to write.

**Fix**:
```python
os.makedirs(image_repo, exist_ok=True)
```

## 🟡 Code Quality Issues

### 8. **Duplicate Imports**
- Line 4 and 8: Both import from `config`
- Line 1 and 9: Both import `os`
- Line 3: `shutil` imported but never used (only in commented code)

**Fix**: Remove duplicates and unused imports.

### 9. **Import Inside Loop** (Line 69)
```python
for post in resp['hits']['hits']:
    import time  # ❌ Should be at top of file
```
**Fix**: Move `import time` to top of file.

### 10. **No Logging**
**Problem**: Only uses `print()` statements. No proper logging like `sync.py` uses.

**Fix**: Add logging:
```python
import logging
logging.basicConfig(filename='logs/html_images.log', level=logging.INFO)
```

### 11. **save_image() Has No Error Handling**
**Problem**: `save_image()` in `sync.py` (lines 81-84) has no error handling:
- Network errors will crash
- File write errors will crash
- No timeout on requests

**Fix**: Update `save_image()` in `sync.py`:
```python
def save_image(url, filename):
    try:
        logging.info("Downloading %s" % url)
        r = requests.get(url, allow_redirects=True, timeout=30)
        r.raise_for_status()  # Raise exception for bad status codes
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(r.content)
        logging.info("Downloaded %s" % filename)
    except Exception as e:
        logging.error("Failed to download %s: %s" % (url, e))
        raise
```

### 12. **No Progress Tracking**
**Problem**: Only prints total count at start. No progress updates during processing.

**Fix**: Add progress counter:
```python
total = len(resp['hits']['hits'])
for i, post in enumerate(resp['hits']['hits'], 1):
    if i % 100 == 0:
        print(f"Processed {i}/{total} posts...")
```

## 📝 Recommended Fixes Before Running

### Quick Fixes (5 minutes):
1. Fix the filename logic bug (lines 80-84)
2. Fix directory permissions or change `image_repo` path
3. Add basic error handling around `save_image()` call
4. Remove duplicate imports
5. Move `import time` to top

### Better Fixes (15 minutes):
6. Add rate limiting (time.sleep)
7. Add directory existence check
8. Add input validation for `src`
9. Add progress tracking

### Production-Ready Fixes (30 minutes):
10. Add pagination/scroll API
11. Add proper logging
12. Improve `save_image()` error handling
13. Add timeout to requests

## 🚀 Safe Version to Run

Here's a minimal safe version you can use:

```python
import os
import time
import logging
from elasticsearch import Elasticsearch
from config import image_repo, host, index
from pyquery import PyQuery as pq
import hashlib
from sync import save_image

logging.basicConfig(filename='logs/html_images.log', level=logging.INFO)
es = Elasticsearch(host=host)

# Ensure directory exists and is writable
os.makedirs(image_repo, exist_ok=True)
if not os.access(image_repo, os.W_OK):
    raise PermissionError(f"Cannot write to {image_repo}")

query = {
    "query": {
        "bool": {
            "must_not": {
                "bool": {
                    "should": [
                        {"match_phrase": {"type.keyword": "photo"}},
                        {"match_phrase": {"type.keyword": "video"}},
                        {"match_phrase": {"type.keyword": "link"}},
                        {"match_phrase": {"type.keyword": "answer"}}
                    ],
                    "minimum_should_match": 1
                }
            }
        }
    },
    "size": 10000,
    "sort": {'liked_timestamp': 'desc'}
}

resp = es.search(index=index, body=query)
total = len(resp['hits']['hits'])
print(f"Found {total} posts to process")

for i, post in enumerate(resp['hits']['hits'], 1):
    if i % 100 == 0:
        print(f"Processed {i}/{total} posts...")
    
    if not post['_source'].get('body'):
        continue
    
    figure = post['_source']['body']
    f = pq(figure)
    
    for image in f("img"):
        src = image.get("src")
        if not src or not src.strip():
            continue
        
        # Handle external vs Tumblr images
        if "media.tumblr.com" not in src:
            m = hashlib.shake_128(str.encode(src)).hexdigest(5)
            filename = image_repo + str(m) + "-" + src.rsplit('/', 1)[1]
        else:
            filename = image_repo + src.rsplit('/', 1)[1]
        
        if not os.path.isfile(filename):
            try:
                print(f"Downloading {src} -> {filename}")
                save_image(src, filename)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logging.error(f"Error downloading {src}: {e}")
                print(f"Error: {e}")
                continue

print(f"Completed processing {total} posts")
```

## ⚠️ Before Running Checklist

- [ ] Fix directory permissions or change `image_repo` path
- [ ] Fix the filename logic bug (lines 80-84)
- [ ] Add error handling around `save_image()`
- [ ] Test with a small subset first (change `size` to 10)
- [ ] Ensure you have disk space
- [ ] Check network connectivity
- [ ] Consider running during off-peak hours (if many images)

