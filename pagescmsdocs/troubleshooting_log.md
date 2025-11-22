# Pages CMS Troubleshooting Log

This document records the specific errors encountered during the Pages CMS integration and how they were resolved.

## Issue 1: List Items Displaying as `[object Object]`

### Symptoms
- In the Pages CMS dashboard, list items (e.g., publications, courses) appeared as `[object Object]` instead of showing their title or summary.
- The content was technically there, but the preview was broken.

### Root Cause
The configuration in `.pages.yml` used an incorrect syntax for the summary template.
- **Incorrect:** `summary: "{title}"` (when `type` was also incorrect)
- **Incorrect:** `type: "list"` (Pages CMS treats `type: "list"` differently than a list of objects)

### Resolution
1.  **Corrected Field Type:** Changed `type: "list"` to `type: "object"` and added a `list` property. This tells Pages CMS that we are defining a list of complex objects, not a simple list of strings.
2.  **Updated Template Syntax:** Changed the summary template to explicitly reference fields using the `{fields.fieldName}` syntax.

**Code Change:**
```yaml
# Before (Broken)
- name: "publications"
  type: "list"
  collapsible:
    summary: "{title}"

# After (Fixed)
- name: "publications"
  type: "object"
  list:
    collapsible:
      summary: "{fields.title}"
```

---

## Issue 2: Runtime Error `Z.options.values.map is not a function`

### Symptoms
- The Pages CMS dashboard would crash with a white screen or error message saying "Something's wrong".
- The browser console showed the error `TypeError: Z.options.values.map is not a function`.

### Root Cause
The `select` field configuration was missing the required `values` key nesting. The code expected `options.values` to be an array, but `options` was defined as an array directly.

### Resolution
Updated the `options` structure for all `select` fields to nest the array under a `values` key.

**Code Change:**
```yaml
# Before (Broken)
options: ["Option A", "Option B"]

# After (Fixed)
options:
  values: ["Option A", "Option B"]
```

## Summary of Fixes

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `[object Object]` | Wrong type & template | Use `type: "object"` + `list` + `{fields.name}` |
| `map is not a function` | Invalid `select` options | Use `options: { values: [...] }` |
