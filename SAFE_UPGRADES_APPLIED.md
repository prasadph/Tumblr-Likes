# Safe Upgrades Applied ✅

## Upgraded Packages

The following packages have been upgraded in `requirements.txt`:

| Package | Old Version | New Version | Notes |
|---------|------------|-------------|-------|
| `certifi` | 2018.8.24 | 2024.2.2 | **6 years of security updates!** |
| `chardet` | 3.0.4 | 5.2.0 | Character encoding detection |
| `future` | 0.16.0 | 0.18.3 | Python 2/3 compatibility |
| `idna` | 2.7 | 3.7 | Internationalized domain names |
| `ipaddress` | 1.0.22 | 1.0.23 | IP address utilities |
| `python-dateutil` | 2.7.3 | 2.9.0 | Date/time utilities |
| `requests` | 2.21.0 | 2.32.3 | HTTP library (security fixes) |
| `six` | 1.11.0 | 1.17.0 | Python 2/3 compatibility |
| `urllib3` | 1.23 | 2.2.2 | **MAJOR** - HTTP client library |

## Installation

If you're running in Docker, you'll need to rebuild or reinstall:

```bash
# Option 1: Rebuild Docker container
docker compose build web
docker compose up -d web

# Option 2: Install in running container
docker compose exec web uv pip install -r requirements.txt
```

If running locally:
```bash
uv pip install -r requirements.txt
```

## Testing Checklist

After installation, test these areas:

1. ✅ **HTTP Requests** - Image downloads, API calls
   - Test: Run `python sync.py` or `flask update-es`
   - Check: Images download successfully

2. ✅ **Web App** - Flask routes work
   - Test: Start Flask app, browse pages
   - Check: All pages load, search works

3. ✅ **Elasticsearch** - Search functionality
   - Test: Search posts, filter by tags/blogs
   - Check: Results return correctly

## Known Issues

- ⚠️ `typed-ast==1.3.1` has compilation issues (dependency of `pylint`)
  - This is a **development tool only** - doesn't affect app functionality
  - If you need pylint, you can upgrade to pylint 3.x which doesn't need typed-ast

## Next Steps

Once you've tested and confirmed everything works:

1. **Phase 2**: Upgrade Flask stack (Flask, Jinja2, Werkzeug, etc.)
2. **Phase 3**: Upgrade OAuth packages (if needed)
3. **Phase 4**: Upgrade other packages

See `UPGRADE_GUIDE.md` for detailed instructions.

