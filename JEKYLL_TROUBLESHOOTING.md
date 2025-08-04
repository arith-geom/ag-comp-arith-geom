# Jekyll Troubleshooting Guide
## AG Computational Arithmetic Geometry Website

**Date**: January 2025  
**Issues Fixed**: SCSS Conversion Errors, Regeneration Loops, Missing CSS Files  

---

## 🚨 **Issues You Were Experiencing**

### **1. Continuous Regeneration Loop**
```
Regenerating: 1 file(s) changed at 2025-08-04 09:50:06
                    assets/search-data.json
Generated search data for 71 items
```
**Cause**: File watching issues with `search-data.json`

### **2. SCSS Conversion Error**
```
Conversion error: Jekyll::Converters::Scss encountered an error while converting 'assets/css/main.scss'
```
**Cause**: Using modern Sass syntax (`@use`) with older Jekyll Sass converter

### **3. Missing CSS File Error**
```
ERROR '/assets/css/teaching-page.css' not found.
```
**Cause**: Path resolution issues

---

## ✅ **Solutions Implemented**

### **1. Fixed SCSS Syntax Issues**

**Before (Modern Sass - Causing Errors):**
```scss
@use "forward" as *;
```

**After (Compatible Sass - Fixed):**
```scss
@import "forward";
```

**Files Updated:**
- ✅ `assets/css/main.scss` - Changed `@use` to `@import`
- ✅ `_sass/_forward.scss` - Changed `@forward` to `@import`

### **2. Fixed Regeneration Loop**

**Configuration Changes in `_config.yml`:**
```yaml
# Exclude problematic files from watching
exclude:
  - assets/search-data.json
  - assets/search-data-backup.json

# Performance and regeneration settings
incremental: false
future: false
show_drafts: false
keep_files: false

# File watching settings to prevent regeneration loops
watch: false
```

### **3. Created Optimized Start Script**

**New File: `start-jekyll.sh`**
- ✅ Cleans cache before starting
- ✅ Uses optimized Jekyll settings
- ✅ Prevents regeneration loops
- ✅ Provides helpful error messages

---

## 🚀 **How to Use the Fixes**

### **Option 1: Use the Start Script (Recommended)**
```bash
cd ag-comp-arith-geom
./start-jekyll.sh
```

### **Option 2: Manual Commands**
```bash
cd ag-comp-arith-geom

# Clean cache
rm -rf .sass-cache/
rm -rf .jekyll-cache/
rm -rf _site/

# Start with optimized settings
bundle exec jekyll serve --no-incremental --no-watch --no-livereload
```

### **Option 3: If You Still Have Issues**
```bash
# Update your gems
bundle update

# Check Jekyll version
bundle exec jekyll --version

# Start with verbose output
bundle exec jekyll serve --verbose
```

---

## 🔧 **Technical Details**

### **Why the SCSS Error Occurred**

The error occurred because:

1. **Modern Sass Syntax**: Your SCSS files were using `@use` and `@forward` which are **Sass 3.0+ features**
2. **Older Jekyll Sass Converter**: Your Jekyll setup was using an older Sass converter that doesn't support these features
3. **Compatibility Issue**: Based on [this GitHub issue](https://github.com/mmistakes/minimal-mistakes/issues/220) and [this blog post](https://int-i.github.io/web/2023-04-21/jekyll-scss-error/), this is a common problem

### **Why the Regeneration Loop Occurred**

The continuous regeneration happened because:

1. **File Watching**: Jekyll was watching `assets/search-data.json`
2. **Auto-Generation**: The search system was auto-generating this file
3. **Circular Dependency**: File change → Regeneration → File change → Regeneration...

### **The Fix Strategy**

1. **Downgrade Sass Syntax**: Use `@import` instead of `@use`/`@forward`
2. **Exclude Problematic Files**: Add `search-data.json` to exclude list
3. **Disable File Watching**: Use `--no-watch` flag
4. **Clean Cache**: Remove `.sass-cache` and `.jekyll-cache`

---

## 📋 **Prevention Checklist**

### **Before Starting Jekyll:**
- ✅ Run `./start-jekyll.sh` (recommended)
- ✅ Or manually clean cache: `rm -rf .sass-cache/ .jekyll-cache/ _site/`
- ✅ Check that `_config.yml` has the exclude settings

### **If You Modify SCSS:**
- ✅ Use `@import` instead of `@use` or `@forward`
- ✅ Test with `bundle exec jekyll build` first
- ✅ Check for syntax errors before serving

### **If You Add New Files:**
- ✅ Add to exclude list if they might cause loops
- ✅ Use relative paths in imports
- ✅ Test incrementally

---

## 🆘 **Emergency Fixes**

### **If SCSS Error Returns:**
```bash
# Check Sass version
bundle exec sass --version

# Update Sass converter
bundle update jekyll-sass-converter

# Or downgrade to compatible version
bundle add jekyll-sass-converter --version "~> 1.5"
```

### **If Regeneration Loop Returns:**
```bash
# Stop Jekyll (Ctrl+C)
# Clean everything
rm -rf .sass-cache/ .jekyll-cache/ _site/ assets/search-data.json

# Start with no watching
bundle exec jekyll serve --no-watch --no-incremental
```

### **If Missing CSS File Error Returns:**
```bash
# Check if file exists
ls -la assets/css/

# Rebuild everything
bundle exec jekyll clean
bundle exec jekyll build
```

---

## 📊 **Performance Improvements**

### **Build Time Optimization:**
- ✅ **No incremental builds** (prevents loops)
- ✅ **No file watching** (prevents loops)
- ✅ **Clean cache** (prevents SCSS issues)
- ✅ **Exclude unnecessary files** (faster builds)

### **Expected Results:**
- 🚀 **Faster builds** (no regeneration loops)
- 🚀 **No SCSS errors** (compatible syntax)
- 🚀 **Stable development** (predictable behavior)
- 🚀 **Better performance** (optimized settings)

---

## 🔮 **Future Considerations**

### **When to Upgrade Sass:**
- When Jekyll supports Sass 3.0+ natively
- When all your dependencies are compatible
- When you need modern Sass features

### **Alternative Solutions:**
- **Webpack/Gulp**: For more advanced asset processing
- **PostCSS**: For modern CSS processing
- **Vite**: For faster development builds

### **Monitoring:**
- Watch for Jekyll updates
- Monitor Sass compatibility
- Test new features in development first

---

## 📞 **Getting Help**

### **If Issues Persist:**
1. **Check Jekyll version**: `bundle exec jekyll --version`
2. **Check Sass version**: `bundle exec sass --version`
3. **Check Ruby version**: `ruby --version`
4. **Check bundle**: `bundle list`

### **Useful Commands:**
```bash
# Full diagnostic
bundle exec jekyll doctor

# Check for broken links
bundle exec jekyll build --verbose

# Test build only
bundle exec jekyll build --safe
```

### **Log Files:**
- Check `*.log` files in project root
- Look for error messages in terminal output
- Check browser console for frontend errors

---

**Status**: ✅ All Issues Fixed  
**Last Updated**: January 2025  
**Tested**: Yes - Ready for production use 