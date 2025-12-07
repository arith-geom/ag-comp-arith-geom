# Pages CMS Configuration Guide

This guide documents the configuration for Pages CMS in this project, specifically focusing on how to correctly set up list widgets and select fields to avoid common errors like `[object Object]` displays and `Z.options.values.map` crashes.

## Key Concepts

### 1. List Widgets (Collections of Objects)

When defining a list of objects (e.g., a list of publications, courses, or members), you must use `type: "object"` and add a `list` property. **Do not use `type: "list"`**.

**Correct Configuration:**

```yaml
fields:
  - name: "my_items"
    label: "My Items"
    type: "object"      # <--- MUST be "object"
    list:               # <--- Add this property
      collapsible:
        summary: "{fields.title}" # <--- Access fields via {fields.fieldName}
        collapsed: true     # <--- Optional: Collapse items by default
    fields:
      - { name: "title", label: "Title", type: "string" }
      - { name: "description", label: "Description", type: "text" }
```

**Common Pitfalls:**

*   **`type: "list"`**: This is incorrect for a list of objects and will often result in display issues or limited functionality.
*   **Summary Template**: Use `{fields.fieldName}` to reference a field within the object. Using just `{fieldName}` might result in `[object Object]`.

### 2. Select Fields

For dropdown menus (`type: "select"`), the options must be nested under a `values` key within the `options` object.

**Correct Configuration:**

```yaml
- name: "status"
  label: "Status"
  type: "select"
  options:
    values: ["Draft", "Published", "Archived"] # <--- Nested under "values"
```

**Common Pitfalls:**

*   **Direct List**: `options: ["A", "B"]` is **incorrect** and will cause the CMS to crash with the error `Z.options.values.map is not a function`.

## Troubleshooting

### Error: `[object Object]` in List Summary
*   **Cause**: The summary template is not correctly accessing the field value.
*   **Fix**: Change the summary template from `{title}` to `{fields.title}` in `.pages.yml`.

### Error: `Z.options.values.map is not a function`
*   **Cause**: The `options` property for a `select` field is defined as a direct array instead of an object with a `values` key.
*   **Fix**: Change `options: [...]` to `options: { values: [...] }`.

## Reference Configuration

Refer to the `.pages.yml` file in the root directory for the live configuration.

### Example: Publications
```yaml
- name: "publications"
  label: "Publications List"
  type: "object"
  list:
    collapsible:
      summary: "{fields.title}"
  fields:
    - { name: "title", label: "Title", type: "string" }
    - { name: "status", label: "Status", type: "select", options: { values: ["Preprint", "Journal Article"] } }
```
