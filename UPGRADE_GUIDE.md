# Package Upgrade Guide

## Summary

I've analyzed your `requirements.txt` and identified packages that can be safely upgraded. Here's what I found:

## ⚠️ **LOCKED Packages** (Must stay at current version)

These packages are locked because they must match your Elasticsearch 6.6.0 server:

- `elasticsearch==6.3.1` - Must match ES server version
- `elasticsearch-dsl==6.2.1` - Must match ES server version

**Note:** If you upgrade Elasticsearch server to 7.x or 8.x, you can upgrade these too.

## ✅ **Safe Upgrades** (Recommended)

### Phase 1: Low Risk - HTTP/Utilities
These are safe to upgrade with minimal testing:

```bash
# HTTP stack
requests==2.32.3          # was 2.21.0
urllib3==2.2.2            # was 1.23 (MAJOR - test SSL/TLS)
certifi==2024.2.2         # was 2018.8.24
chardet==5.2.0            # was 3.0.4
idna==3.7                 # was 2.7

# Utilities
python-dateutil==2.9.0    # was 2.7.3
six==1.17.0               # was 1.11.0
future==0.18.3            # was 0.16.0
ipaddress==1.0.23         # was 1.0.22
```

### Phase 2: Medium Risk - Flask Stack
Upgrade these together (they're interdependent):

```bash
Flask==3.0.0              # was 1.0.2 (MAJOR)
Jinja2==3.1.4             # was 2.10 (MAJOR)
Werkzeug==3.0.3           # was 0.14.1 (MAJOR)
itsdangerous==2.1.2       # was 0.24 (MAJOR)
click==8.1.7              # was 6.7 (MAJOR)
```

**Breaking Changes to Watch:**
- Flask 3.0 removed some deprecated features
- Some template syntax may need updates
- Test all routes thoroughly

### Phase 3: OAuth (if needed)
Only if you use OAuth features:

```bash
requests-oauthlib==1.3.1  # was 1.0.0
oauthlib==3.2.2           # was 2.1.0 (MAJOR)
```

**Note:** Removed unused packages:
- ❌ `Flask-JWT-Extended` - Not used in codebase
- ❌ `PyJWT` - Not used in codebase  
- ❌ `marshmallow` - Not used in codebase
- ❌ `redis` - Not used in codebase
- ❌ `rq` - Not used in codebase

### Phase 4: Other Packages
```bash
pyquery==1.4.3            # Keep at 1.4.3 (2.0.0 has breaking changes)
PyTumblr==0.0.8           # Check if maintained
```

### Development Tools (Optional)
```bash
pylint==3.2.3             # was 2.1.1 (requires astroid 3.x)
astroid==3.2.2            # was 2.0.4 (required by pylint 3.x)
autopep8==2.0.4           # was 1.4.1
isort==5.13.2             # was 4.3.4
pycodestyle==2.11.1       # was 2.4.0
```

## 🚀 **How to Upgrade Using `uv`**

### Option 1: Upgrade All at Once (Recommended for testing)
```bash
# Backup current requirements
cp requirements.txt requirements.txt.backup

# Use the upgraded requirements file
cp requirements_upgraded.txt requirements.txt

# Install with uv
uv pip install -r requirements.txt
```

### Option 2: Phased Upgrade (Safer)
```bash
# Phase 1: HTTP/Utilities only
uv pip install --upgrade requests urllib3 certifi chardet idna python-dateutil six future ipaddress

# Test your app, then continue...

# Phase 2: Flask stack
uv pip install --upgrade Flask Jinja2 Werkzeug itsdangerous click

# Test thoroughly, then continue...

# Phase 3: OAuth/JWT
uv pip install --upgrade requests-oauthlib oauthlib PyJWT Flask-JWT-Extended

# Test authentication, then continue...

# Phase 4: Others
uv pip install --upgrade marshmallow redis rq
```

### Option 3: Update requirements.txt incrementally
```bash
# Edit requirements.txt manually, then:
uv pip install -r requirements.txt
```

## 🧪 **Testing Checklist**

After upgrading, test:

1. ✅ All Flask routes work
2. ✅ Template rendering (Jinja2 changes)
3. ✅ Authentication/authorization (JWT/OAuth)
4. ✅ Elasticsearch queries still work
5. ✅ Image downloads (requests/urllib3)
6. ✅ Tumblr API calls (PyTumblr)
7. ✅ Background jobs (rq/redis)

## 📝 **Files Created**

- `requirements_upgraded.txt` - Full upgraded requirements
- `upgrade_analysis.md` - Detailed analysis
- `UPGRADE_GUIDE.md` - This file

## ⚡ **Quick Start**

```bash
# 1. Backup current setup
cp requirements.txt requirements.txt.backup

# 2. Test upgrade in a virtual environment first
python -m venv test_env
source test_env/bin/activate  # or `test_env\Scripts\activate` on Windows
uv pip install -r requirements_upgraded.txt

# 3. Run your tests
# 4. If all good, apply to main environment
```

## 🔄 **Rollback**

If something breaks:
```bash
cp requirements.txt.backup requirements.txt
uv pip install -r requirements.txt
```

