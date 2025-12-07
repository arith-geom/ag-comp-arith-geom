# Pages CMS Best Practices

Follow these guidelines to ensure the Pages CMS configuration remains stable and error-free.

## 1. Configuration Structure

### Always Use `type: "object"` for Collections
When defining a collection of items (like publications, members, or projects), always use the `type: "object"` combined with the `list` property.

**Why?**
The `type: "list"` shorthand is often intended for simple lists of strings (like tags). For structured content with multiple fields, `type: "object"` is the robust and correct choice.

**Template:**
```yaml
- name: "collection_name"
  label: "My Collection"
  type: "object"
  list:
    collapsible:
      summary: "{fields.title}" # Always use {fields.fieldName}
  fields:
    - { name: "title", label: "Title", type: "string" }
```

### Strict Syntax for Select Fields
Never pass a raw array to `options`. Always wrap it in an object.

**Why?**
Pages CMS expects an object configuration. Passing an array directly causes the internal code to fail when it tries to access `.values`.

**Template:**
```yaml
type: "select"
options:
  values: ["Option 1", "Option 2"]
```

## 2. Workflow

### Verify Locally (If Possible)
If you have a way to run Pages CMS locally (e.g., via a proxy), do so before pushing. If not, push to a separate branch (like `testing-cms`) to verify changes without breaking the main site.

### Check the Console
If the CMS screen goes blank or shows a generic error, open the browser's Developer Tools (F12) -> Console. Look for red error messages.
- `map is not a function` usually means a data structure mismatch (array vs object).
- `undefined` errors usually mean a missing field name or incorrect path.

## 3. Documentation

### Keep `.pages.yml` Comments Updated
If you add complex logic or a new field type, add a comment in `.pages.yml` explaining why it's configured that way.

### Refer to Official Docs
Pages CMS documentation is the source of truth. If a configuration looks "standard" but fails, check if the API has changed.
- [Pages CMS Configuration Docs](https://pagescms.org/docs/configuration/)
