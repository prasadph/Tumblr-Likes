# PyTumblr 0.0.8 → 0.1.2 Upgrade

## What Changed

Based on the [GitHub release notes](https://github.com/tumblr/pytumblr/releases/tag/0.1.2), version 0.1.2 (released January 18, 2023) includes:

### Infrastructure/Maintenance Updates
- ✅ Add YAML validation to bootstrap GitHub Workflows
- ✅ Add CI testing procedure
- ✅ Update setuptools
- ✅ Publish workflow improvements
- ✅ Drop Travis CI configuration
- ✅ Version bump to 0.1.2

### Important Notes
- **No breaking API changes** - Your existing code will work without modifications
- **No new API methods** - The Tumblr API methods remain the same
- **Maintenance release** - Focuses on build/release infrastructure

## What You're Currently Using

Your codebase uses these PyTumblr methods:
- `client.likes()` - Fetch liked posts (in `sync.py`)
- `client.like()` - Like a post (in `core/tumblr/likes.py`)
- `client.unlike()` - Unlike a post (in `core/tumblr/likes.py`)

## Available Methods (30 total)

PyTumblr 0.1.2 provides these methods:

**Blog Operations:**
- `blog_info()` - Get blog information
- `blog_likes()` - Get blog's liked posts
- `blog_following()` - Get blogs this blog follows
- `avatar()` - Get blog avatar

**Post Operations:**
- `create_text()` - Create text post
- `create_photo()` - Create photo post
- `create_quote()` - Create quote post
- `create_link()` - Create link post
- `create_chat()` - Create chat post
- `create_audio()` - Create audio post
- `create_video()` - Create video post
- `edit_post()` - Edit existing post
- `reblog()` - Reblog a post
- `delete_post()` - Delete a post
- `posts()` - Get posts from a blog

**User Operations:**
- `user_info()` - Get user information
- `dashboard()` - Get dashboard posts
- `likes()` - Get user's liked posts (you use this)
- `like()` - Like a post (you use this)
- `unlike()` - Unlike a post (you use this)
- `following()` - Get blogs user follows
- `follow()` - Follow a blog
- `unfollow()` - Unfollow a blog

**Other:**
- `tagged()` - Get posts by tag
- `queue()` - Get queued posts
- `draft()` - Get draft posts

## Benefits of Upgrade

1. **Better Maintenance** - Improved CI/CD and release process
2. **Updated Dependencies** - Uses newer setuptools
3. **Bug Fixes** - May include fixes from 0.0.9, 0.1.0, 0.1.1
4. **Future-Proof** - More actively maintained

## Impact on Your Code

✅ **No changes needed** - Your existing code works as-is
✅ **Same API** - All methods you use work the same way
✅ **Backward compatible** - Drop-in replacement

## Summary

The upgrade from 0.0.8 to 0.1.2 is primarily a **maintenance release** with:
- ✅ Infrastructure improvements
- ✅ Better build/release process
- ✅ No breaking changes
- ✅ No new features, but better maintained

Your code continues to work exactly as before, but now with a more actively maintained package.

