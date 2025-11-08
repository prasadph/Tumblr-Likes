# Next Steps - Package Upgrades

## ✅ Phase 1 Complete: Safe Upgrades

**Completed:**
- ✅ HTTP/SSL stack upgraded (requests, certifi, chardet, idna, urllib3)
- ✅ Utilities upgraded (python-dateutil)
- ✅ Installed in Docker container
- ✅ requirements.txt & pyproject.toml synchronized
- ✅ Dependency warnings fixed

**Current versions in Docker:**
- `requests`: 2.27.1 (Python 3.6 compatible)
- `certifi`: 2025.4.26
- `chardet`: 4.0.0
- `urllib3`: 1.26.20
- `idna`: 3.10
- `python-dateutil`: 2.9.0

---

## 🧪 Step 1: Test Current Upgrades (Recommended)

Before proceeding, test that everything works:

```bash
# 1. Test sync functionality
docker compose exec web python sync.py

# 2. Test web app
# Open http://localhost:5000 in browser
# Test: search, filters, image viewing, like/unlike

# 3. Test image downloads
docker compose exec web flask update-es

# 4. Check for any errors in logs
docker compose logs web | tail -50
```

**If everything works, proceed to Phase 2.**

---

## 🚀 Phase 2: Flask Stack Upgrades (Medium Risk)

Upgrade the core Flask framework and related packages:

### Packages to Upgrade:
- `Flask`: 1.0.2 → 3.0.0 (MAJOR)
- `Jinja2`: 2.10 → 3.1.4 (MAJOR)
- `Werkzeug`: 0.14.1 → 3.0.3 (MAJOR)
- `itsdangerous`: 0.24 → 2.1.2 (MAJOR)
- `click`: 6.7 → 8.1.7 (MAJOR)

### Breaking Changes to Watch:
- Flask 3.0 removed some deprecated features
- Template syntax may need updates
- Some API changes in Werkzeug

### How to Proceed:

**Option A: Manual Upgrade (Recommended for testing)**
```bash
# Update requirements.txt manually
# Then install in Docker:
docker compose exec web pip install --upgrade Flask Jinja2 Werkzeug itsdangerous click

# Test thoroughly
docker compose restart web
```

**Option B: Use requirements_upgraded.txt**
```bash
# Copy upgraded requirements
cp requirements_upgraded.txt requirements.txt

# Install in Docker
docker compose exec web pip install -r requirements.txt

# Test thoroughly
docker compose restart web
```

### Testing Checklist:
- [ ] All Flask routes work
- [ ] Templates render correctly
- [ ] Search functionality works
- [ ] Image viewing works
- [ ] Like/Unlike buttons work
- [ ] No template errors
- [ ] No deprecation warnings

---

## 📦 Phase 3: OAuth Packages (If Needed)

Only if you use OAuth features:

- `requests-oauthlib`: 1.0.0 → 1.3.1
- `oauthlib`: 2.1.0 → 3.2.2 (MAJOR)

Test authentication flows carefully.

---

## 🔧 Phase 4: Other Packages

- `pyquery`: Keep at 1.4.3 (2.0.0 has breaking changes)
- `PyTumblr`: 0.0.8 (check if maintained, may need fork)

---

## 📝 Recommended Approach

1. **Test Phase 1** (current safe upgrades) - ✅ DONE
2. **Proceed to Phase 2** (Flask stack) - Test each package upgrade
3. **Test thoroughly** after Phase 2
4. **Proceed to Phase 3** (OAuth) if needed
5. **Final testing** of entire application

---

## ⚠️ Important Notes

- **Python 3.6 Limitation**: Your Docker container uses Python 3.6
  - Some packages may have version limits
  - Consider upgrading Docker to Python 3.9+ for latest packages
  - Or accept compatible versions (like requests 2.27.1)

- **Elasticsearch Locked**: Must stay at 6.3.1/6.2.1 (matches ES server 6.6.0)

- **Backup First**: Always test in Docker before applying to production

---

## 🎯 Quick Start: Phase 2

If you're ready to proceed with Flask upgrades:

```bash
# 1. Update requirements.txt with Flask stack versions
# 2. Install in Docker
docker compose exec web pip install --upgrade Flask==3.0.0 Jinja2==3.1.4 Werkzeug==3.0.3 itsdangerous==2.1.2 click==8.1.7

# 3. Restart and test
docker compose restart web

# 4. Test the application
# Open http://localhost:5000
```

See `UPGRADE_GUIDE.md` for detailed instructions.

