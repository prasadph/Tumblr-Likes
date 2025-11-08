# Remaining Package Upgrades

## ✅ Safe to Upgrade

### 1. Development Tools (Optional)
These are only used for code quality, not runtime:

- **autopep8**: 1.4.1 → 2.3.2 (MAJOR)
- **isort**: 4.3.4 → 7.0.0 (MAJOR) 
- **pylint**: 2.1.1 → 4.0.2 (MAJOR)

**Note:** pylint 4.x requires astroid 4.x (will be auto-installed)

### 2. Minor Updates

- **python-dateutil**: 2.9.0 → 2.9.0.post0 (patch fix)

## ⚠️ Keep As-Is

- **pyquery**: 1.4.3 (2.0.1 available but has breaking changes)
- **PyTumblr**: 0.0.8 (may be unmaintained, check if newer version exists)

## 🔒 Locked (Cannot Upgrade)

- **elasticsearch**: 6.3.1 (must match ES server 6.6.0)
- **elasticsearch-dsl**: 6.4.0 (compatible with ES 6.6.0 and Python 3.10)

## 🎯 Recommended Next Steps

### Option 1: Upgrade Dev Tools (Recommended)
```bash
docker compose exec web pip install --upgrade autopep8==2.3.2 isort==7.0.0 pylint==4.0.2
```

### Option 2: Upgrade python-dateutil (Minor)
```bash
docker compose exec web pip install --upgrade python-dateutil==2.9.0.post0
```

### Option 3: Both
```bash
docker compose exec web pip install --upgrade autopep8==2.3.2 isort==7.0.0 pylint==4.0.2 python-dateutil==2.9.0.post0
```

## 📊 Summary

**Already Upgraded:**
- ✅ Flask: 1.0.2 → 3.0.0
- ✅ Jinja2: 2.10 → 3.1.4
- ✅ requests: 2.21.0 → 2.32.3
- ✅ elasticsearch-dsl: 6.2.1 → 6.4.0 (Python 3.10 compatibility)
- ✅ Python: 3.6 → 3.10

**Remaining:**
- Dev tools (optional)
- python-dateutil (minor patch)
- pyquery (keep at 1.4.3)
- PyTumblr (check if maintained)

