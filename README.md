# AG Computational Arithmetic Geometry - Official Website

**This is the official website for the Computational Arithmetic Geometry research group at Heidelberg University.**

## About This Website

This website serves as the central hub for the **Arbeitsgruppe (AG) Computational Arithmetic Geometry** led by Prof. Dr. Gebhard Böckle at the Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University.

## What You'll Find Here

All information about our research group is available directly on this website:

- **Research Areas**: Detailed information about our work in algebraic number theory, arithmetic geometry, Galois representations, modular forms, elliptic curves, and function field arithmetic
- **Publications**: Complete list of our research publications and academic contributions
- **Team Members**: Information about our current and former group members
- **Teaching**: Courses and educational materials
- **Contact Information**: How to reach us

## Research Focus

Our group focuses on:
- Galois representations and their connections to modular forms and elliptic curves
- Deformation theory of Galois representations
- L-functions and Drinfeld modular forms in function field arithmetic
- Computational methods in number theory and arithmetic geometry

## Group Information

- **Location**: Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University
- **Contact**: arithgeo@iwr.uni-heidelberg.de
- **Led by**: Prof. Dr. Gebhard Böckle

---

## Technical Setup (For Development)

This website is built with Jekyll and hosted on GitHub Pages. If you need to work on the website development, follow these steps:

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/placeholder-ag-comp-arith-geom/placeholder-ag-comp-arith-geom.github.io.git
   cd placeholder-ag-comp-arith-geom.github.io
   ```

2. **Run the setup script:**
   ```bash
   ./scripts/setup.sh
   ```

3. **Start the development server:**
   ```bash
   bundle exec jekyll serve
   ```

3. **View the website:**
   Open your browser and visit `http://localhost:4000`

### Project Structure

- `_pages/` - Main website pages
- `_research/` - Research content and descriptions
- `_publications/` - Publication data and formats
- `_members/` - Team member information
- `_includes/` - Reusable HTML components
- `assets/` - CSS, JavaScript, and image files

---

## Content Management with PagesCMS

This website's content is managed using PagesCMS, a user-friendly, Git-based content management system. This allows you to edit the content of the website without needing to write any code.

### How to Edit Content

1.  **Log in to PagesCMS**: Go to [app.pagescms.org](https://app.pagescms.org/) and log in with your GitHub account.
2.  **Select Your Repository**: Once logged in, you should see this repository in your list of sites. Select it to open the CMS interface.
3.  **Navigate and Edit**: You will see a sidebar with links to the different content types you can edit (e.g., Publications, Members, Teaching, etc.). Click on a section to see the entries, and then click on an entry to open the editor.
4.  **Save Changes**: After making your changes, click the "Save" button. PagesCMS will automatically create a new commit in the repository with your updates. The website will then rebuild and your changes will be live.

The configuration for PagesCMS is stored in the `.pages.yml` file in this repository.