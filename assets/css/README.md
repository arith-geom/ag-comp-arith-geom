# CSS Structure and Organization

## File Organization

This project uses a structured CSS organization to separate concerns and make development easier:

### Main Files
- **`main.scss`** - Main entry point with all styles and imports
- **`style.scss`** - Alternative entry point (check which one is actually used by Jekyll)

### Directory Structure

#### `assets/css/`
- **`components/`** - Reusable component styles
  - `_forward.scss` - Forwards all component styles
  - `_variables.scss` - CSS custom properties and variables
  - `_themes.scss` - Theme-related styles (dark mode, etc.)
  - `search.scss` - Search functionality styles
- **`pages/`** - Page-specific styles
  - `_teaching-page.scss` - **ACTIVE** teaching page styles
- **`syntax-highlighting/`** - Code syntax highlighting themes
- **`vendor/`** - Third-party CSS libraries

#### `_sass/` (Legacy/Source Files)
- Contains source SCSS files, some may be duplicates
- **⚠️ WARNING**: Files in `_sass/` are NOT automatically compiled
- Always check if your changes are in the correct `assets/css/` location

## Active vs Inactive Files

### ✅ ACTIVE FILES (Compiled and Used)
- `assets/css/pages/_teaching-page.scss` - Teaching page styles
- `assets/css/components/_variables.scss` - CSS variables
- `assets/css/components/_themes.scss` - Theme styles

### ❌ INACTIVE FILES (Not Compiled)
- Files in `_sass/` directory are legacy and should not be edited
- All active styles are now in the `assets/css/` directory structure

## How to Make Changes

1. **Always check this README first** to find the correct file location
2. **Edit files in `assets/css/`, not `_sass/`**
3. **Test your changes** - the site uses Jekyll which may need rebuilding

## Recent Changes
- **2024-XX-XX**: Removed duplicate `_sass/_teaching-page.scss` file to eliminate confusion
- **2024-XX-XX**: Fixed teaching page styles location confusion
- **2024-XX-XX**: Added clear warnings to duplicate files
- **2024-XX-XX**: Updated forward file to correctly reference page styles

## Build Process

The CSS is compiled using Jekyll's built-in SCSS processor. Changes to files in `assets/css/` will be automatically included in the build process.
