# Pages CMS Architecture Overview

This document explains how Pages CMS integrates with this Jekyll website.

## High-Level Flow

1.  **Content Storage**: All content is stored as static files in the GitHub repository.
    -   **Data Files**: `_data/*.yml` (Structured data like publications, members)
    -   **Pages**: `_pages/*.md` (Markdown content for specific pages)
2.  **CMS Interface**: Pages CMS (`admin/index.html` or similar entry point) runs in the browser. It uses the GitHub API to read and write these files directly.
3.  **Configuration**: The `.pages.yml` file tells Pages CMS how to interpret the files in the repository. It maps the raw YAML/Markdown data to user-friendly forms.
4.  **Build Process**: When Pages CMS saves a change, it commits directly to the repository. This triggers a GitHub Actions build (or Jekyll build) which regenerates the static site.

## Key Components

### `.pages.yml`
The brain of the CMS. It defines:
-   **Collections**: Groups of content (e.g., "Publications").
-   **Fields**: The input types (text, image, select) for each piece of content.
-   **Paths**: Where to find the files in the repo (e.g., `path: "_data/publications.yml"`).

### `_data/` Directory
This project relies heavily on Jekyll Data Files.
-   Instead of having one markdown file per publication, we have a single `publications.yml` file containing a list of all publications.
-   Pages CMS is configured to edit this *single file* as a list of objects, rather than creating new files for each entry.

### `_pages/` Directory
Contains individual markdown pages (Home, Research, Contact).
-   Pages CMS edits the Front Matter (YAML header) and the Body (Markdown content) of these files.

## Diagram

```mermaid
graph TD
    User[User] -->|Edits Content| CMS[Pages CMS Interface]
    CMS -->|Reads Config| Config[.pages.yml]
    CMS -->|GitHub API| Repo[GitHub Repository]
    Repo -->|Contains| Data[_data/*.yml]
    Repo -->|Contains| Pages[_pages/*.md]
    Repo -->|Trigger| Build[Jekyll Build]
    Build -->|Generates| Site[_site/ (HTML/CSS)]
```
