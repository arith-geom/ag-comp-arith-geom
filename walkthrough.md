# Design Updates Walkthrough

I have implemented the requested design changes to improve the website's aesthetics and consistency.

## Changes Implemented

### 1. Footer Redesign
- **Background**: Changed to Light Gray (`var(--gray-100)`).
- **Text Color**: Changed to Dark (`var(--gray-900)`) for better contrast.
- **Logo**: Applied `mix-blend-mode: multiply` to the IWR/Uni logo to make the white background transparent against the light gray footer.
- **IWR Link**: Added a direct link to the IWR website in the footer text.

### 2. Border Radius Consistency
- **Teaching, Publications, Members**: Standardized to use the smallest radius (`v.$radius-sm` / 8px).
- **Home, Research, Links (Outer)**: Standardized to use a medium radius (`v.$radius-md` / 16px), slightly smaller than the previous large radius.
- **Links (Inner)**: Updated to match the Teaching page radius (`v.$radius-sm` / 8px).

### 3. Teaching Subpages
- **Course Title**: Reduced font size from `display-5` to `h2` to better handle long titles.
- **Year**: Removed the redundant "Year" field (Semester is sufficient).
- **Details Box**: Updated styling to match the "cleaner" look of the Publications details box:
    - Labels are now `d-block text-dark small` (not uppercase).
    - Values are `text-dark` (darker than previous gray).

### 4. Publications Subpages
- **Details Box**: Darkened the text color (`text-secondary` -> `text-dark`) to improve readability.

### 5. Members Subpages
- **Text Color**: Darkened gray text (`text-muted`, `text-secondary`) to `text-dark` throughout the profile (Role, Bio, Contact, Education, Publications) to match the header color and improve readability.

## Verification
- **Footer**: Verified code changes in `_sass/_themes.scss`, `_sass/_footer.scss`, and `_includes/layout/footer.liquid`.
- **Border Radius**: Verified updates in `_sass/_home.scss`, `_sass/_links.scss`, and `_sass/_publications.scss`.
- **Subpages**: Verified template updates in `_layouts/teaching_subpage.html`, `_layouts/publication_subpage.html`, and `_layouts/member.html`.
