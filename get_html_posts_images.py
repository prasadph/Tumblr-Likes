import os
from elasticsearch import Elasticsearch
from config import image_repo, host, index
from pyquery import PyQuery as pq
import hashlib
from sync import save_image

es = Elasticsearch(host=host)

# directory_in_str = "/home/prasad/tumblr/"
# directory = os.fsencode(directory_in_str)
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     query = {
#         "query": {
#             "match_phrase": {
#                 "photos.original_size.url": filename
#             }
#         },
#         "size": 0
#     }
#     resp = es.search(index="tumblr_likes_3", body=query)
#     if resp["hits"]["total"] == 0:
#         print(filename)
#         shutil.move(directory_in_str + filename, "extra")
query = {
    "query": {
        "bool": {
            "must_not":{
                 "bool": {
            "should": [
              {
                "match_phrase": {
                  "type.keyword": "photo"
                }
              },
              {
                "match_phrase": {
                  "type.keyword": "video"
                }
              },
              {
                "match_phrase": {
                  "type.keyword": "link"
                }
              },
              {
                "match_phrase": {
                  "type.keyword": "answer"
                }
              }
            ],
            "minimum_should_match": 1
          }

            }
        }
    },
    "size": 1000,
    "sort": {'liked_timestamp': 'asc'}  # Oldest first - process already-done posts quickly, then new ones
}

# Get total count first for progress estimation
count_query = query.copy()
count_query["size"] = 0
count_resp = es.search(index=index, body=count_query)
total_posts = count_resp['hits']['total']['value'] if isinstance(count_resp['hits']['total'], dict) else count_resp['hits']['total']
estimated_batches = (total_posts + 999) // 1000  # Round up

print("=" * 60)
print("Starting to process HTML post images...")
print(f"Total posts to process: {total_posts} (estimated {estimated_batches} batches)")
print("=" * 60)

# Initial search with scroll
resp = es.search(index=index, body=query, scroll="10m")
scroll_id = resp['_scroll_id']
total_processed = 0
batch_num = 1
images_found = 0
images_downloaded = 0
images_skipped = 0
posts_with_images = 0

# Process all batches using scroll API
while len(resp['hits']['hits']) > 0:
    batch_size = len(resp['hits']['hits'])
    total_processed += batch_size
    remaining_batches = estimated_batches - batch_num
    
    posts_in_batch = 0
    for post in resp['hits']['hits']:
        posts_in_batch += 1
        body = post['_source'].get('body')
        if not body:
            continue
        
        # Quick check: skip if body doesn't contain 'img' tag (faster than parsing)
        if '<img' not in body and '<IMG' not in body:
            continue
        
        # Parse HTML only if we know there might be images
        try:
            f = pq(body)
            images_in_post = f("img")
        except Exception as e:
            print(f"  Warning: Error parsing HTML for post: {e}")
            continue
        
        if len(images_in_post) > 0:
            posts_with_images += 1
            
            for image in images_in_post:
                src = image.get("src")
                if not src or not src.strip():
                    continue
                
                images_found += 1
                
                # Determine filename (fix the logic bug)
                if "media.tumblr.com" not in src:
                    m = hashlib.shake_128(str.encode(src)).hexdigest(5)
                    filename = image_repo + str(m) + "-" + src.rsplit('/', 1)[1]
                else:
                    filename = image_repo + src.rsplit('/', 1)[1]
                
                # Fast file existence check
                if not os.path.isfile(filename):
                    try:
                        save_image(src, filename)
                        images_downloaded += 1
                        if images_downloaded % 10 == 0:
                            print(f"  [Downloaded {images_downloaded} images so far...]")
                    except Exception as e:
                        print(f"  Error downloading image: {e}")
                else:
                    images_skipped += 1
        
        # Show activity every 100 posts
        if posts_in_batch % 100 == 0:
            print(f"  Processing post {posts_in_batch}/{batch_size} in batch {batch_num}...")
    
    # Progress update with remaining batches
    progress_pct = (total_processed / total_posts * 100) if total_posts > 0 else 0
    print(f"Batch {batch_num}/{estimated_batches} ({progress_pct:.1f}%) | "
          f"{batch_size} posts | Total: {total_processed}/{total_posts} | "
          f"Images: {images_downloaded}↓ {images_skipped}✓ {images_found} total | "
          f"Remaining: ~{remaining_batches} batches")
    
    # Get next batch with error handling
    batch_num += 1
    print(f"  Fetching next batch ({batch_num}/{estimated_batches})...")
    try:
        resp = es.scroll(scroll_id=scroll_id, scroll="10m")
        scroll_id = resp['_scroll_id']
        print(f"  ✓ Retrieved {len(resp['hits']['hits'])} posts")
    except Exception as e:
        print(f"  ✗ Error fetching next batch: {e}")
        break

# Final summary
print("=" * 60)
print("Processing completed!")
print(f"Total posts processed: {total_processed}")
print(f"Posts with images: {posts_with_images}")
print(f"Total images found: {images_found}")
print(f"Images downloaded: {images_downloaded}")
print(f"Images skipped (already exist): {images_skipped}")
print("=" * 60)
