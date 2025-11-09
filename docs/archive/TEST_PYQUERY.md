# Testing pyquery

## Quick Tests

### 1. Basic Functionality Test
```bash
docker compose exec web python -c "
from pyquery import PyQuery as pq
html = '<div><img src=\"test.jpg\"/></div>'
doc = pq(html)
print('Found', len(doc('img')), 'image(s)')
"
```

### 2. Test ttimages Filter
```bash
docker compose exec web python -c "
import sys; sys.path.insert(0, '/app')
from views.likes import get_modifed_body
html = '<p>Test</p><img src=\"https://media.tumblr.com/test.jpg\"/>'
result = get_modifed_body(html)
print('Filter output length:', len(result))
print('Contains image containers:', 'post-image-container' in result)
"
```

### 3. Test Real-World Usage
```bash
# Test the actual script that uses pyquery
docker compose exec web python get_html_posts_images.py
```

## Real-World Testing

### Test via Web Interface
1. Open http://localhost:5000
2. Browse to a text post that has embedded images
3. Verify images are displayed correctly
4. Check browser console for any errors

### Test Image Extraction Script
```bash
# Run the script that extracts images from HTML posts
docker compose exec web python get_html_posts_images.py
```

This will:
- Find all text posts with images
- Extract image URLs using pyquery
- Download images to your image_repo directory

## Expected Behavior

✅ **Working correctly if:**
- Images are found in HTML posts
- Image URLs are extracted properly
- Images display in the web interface
- No errors in logs

❌ **Issues if:**
- No images found when they exist
- AttributeError or ImportError
- Images not displaying in web interface

