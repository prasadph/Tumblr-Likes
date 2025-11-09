# pyquery Upgrade Analysis

## Current Usage

`pyquery` is used in **2 files**:

### 1. `views/likes.py` - `ttimages` filter
```python
from pyquery import PyQuery as pq

@app.template_filter('ttimages')
def get_modifed_body(body):
    f = pq(body)  # Parse HTML string
    for image in f("img"):  # Find img tags
        src = image.get("src")  # Get src attribute
        # ... process image
```

### 2. `get_html_posts_images.py` - Image extraction
```python
from pyquery import PyQuery as pq

f = pq(body)  # Parse HTML string
images_in_post = f("img")  # Find img tags
for image in images_in_post:
    src = image.get("src")  # Get src attribute
    # ... download image
```

## Breaking Changes in pyquery 2.0

### 1. **URL Handling** (Not affecting us)
- **Old**: `PyQuery("http://example.com")` would fetch URL
- **New**: Must use `PyQuery(url="http://example.com")`
- **Impact**: ✅ **None** - We only parse HTML strings, not URLs

### 2. **Python Version Support**
- **Dropped**: Python 3.5, 3.6, 3.7
- **Required**: Python 3.8+
- **Impact**: ✅ **OK** - We're on Python 3.10

### 3. **HTML/XML Parser**
- HTML parser with XML files no longer tested
- **Impact**: ✅ **None** - We only parse HTML, not XML

## Compatibility Check

✅ **Our usage is compatible with pyquery 2.0!**

We only use:
- `pq(html_string)` - ✅ Still works
- `f("img")` - ✅ Still works  
- `image.get("src")` - ✅ Still works

## Recommendation

**Safe to upgrade to pyquery 2.0.1!**

The breaking changes don't affect our usage pattern. We:
- ✅ Only parse HTML strings (not URLs)
- ✅ Use Python 3.10 (meets requirements)
- ✅ Only parse HTML (not XML)

## Upgrade Command

```bash
docker compose exec web pip install --upgrade pyquery==2.0.1
```

## Testing After Upgrade

Test these areas:
1. ✅ Image extraction in text posts (ttimages filter)
2. ✅ Image downloading script (get_html_posts_images.py)
3. ✅ Verify images display correctly in web interface

