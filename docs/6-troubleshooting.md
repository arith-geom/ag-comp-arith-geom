# 🛡️ Troubleshooting & "The Guardian"

This website is protected by an automated system we call **"The Guardian"**.

Its job is to prevent errors (like typos, broken links, or bad filenames) from reaching the live website. It runs every time you make a change or save content in the CMS.

---

## 🛑 How it Works

1.  **You Save a Change** (in Pages CMS or GitHub).
2.  **The Guardian Wakes Up**: It checks your changes for:
    *   Syntactical errors (YAML, SCSS).
    *   Missing required data (Names, Titles).
    *   Bad filenames (Spaces, special characters).
    *   Asset sizes (Images > 2MB).
    *   Broken links (404 errors).
3.  **Pass or Fail**:
    *   ✅ **Pass**: Your changes are built and deployed to the live site.
    *   ❌ **Fail**: The deployment **STOPS**. The live site remains unchanged (safe).

---

## 🔍 How to Spot an Error

If your changes don't show up on the website after a few minutes, the Guardian probably stopped them.

1.  Go to the **[Actions Tab](https://github.com/arith-geom/ag-comp-arith-geom/actions)** on GitHub.
2.  Look at the latest run.
    *   **Green Checkmark**: Success. (Maybe wait a minute for cache to clear).
    *   **Red X**: Failed. Click on it.
3.  Click the **"Guardian"** step that failed (it will be red).

---

## 🛠️ Common Errors & Fixes

Here is how to translate "Computer Speak" to English:

### 1. "Unsafe filename found"
> `[ERROR] Unsafe filename found: assets/uploads/My CV.pdf`

**Problem**: You uploaded a file with a space or special character in the name.
**Fix**: Rename the file to `My_CV.pdf` (use underscores or dashes) and re-upload it.

### 2. "Missing field"
> `Publication #5: Missing 'title'. (Context: authors='Smith'...)`

**Problem**: You added an entry (like a publication or member) but left a required field empty.
**Fix**: Go back to the CMS, find the entry (e.g., the publication by Smith), add the Title, and save.

### 3. "Syntax Error"
> `members.yml:10:2: syntax error` or `mapping values are not allowed here`

**Problem**: There is a typo in the code structure (usually in YAML files).
**Fix**: Look at line 10. Did you forget a colon? Did you mess up the indentation? Compare it to the lines above it.

### 4. "Link Check Failed"
> `External link https://example.com/foo failed: 404 No Found`

**Problem**: You pasted a link that doesn't exist.
**Fix**: Correct the URL.

### 5. "Large file warning"
> `[WARNING] Large file (5.20 MB): assets/uploads/thesis.pdf`

**Problem**: The file is huge. It will slow down the site.
**Fix**: Compress the PDF or image and re-upload it. (Note: This is a *Warning*, so it won't stop the site, but you should fix it).

---

## ⚡ Running Checks Manually

If you are a developer or running the site locally, you can run these checks yourself:

```bash
# Validate content (Data & Assets)
python3 scripts/validate.py

# Clean up unused media (Dry Run)
python3 scripts/cleanup_unused_media.py
```
