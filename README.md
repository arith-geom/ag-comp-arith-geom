# AG Computational Arithmetic Geometry - Official Website

**This is the official website for the Computational Arithmetic Geometry research group at Heidelberg University.**

## 📚 Documentation

**[👉 Read the User Guide (docs/)](docs/README.md)**
Learn how to manage members, publications, teaching, and other content using the Pages CMS interface.

**[🛡️ Troubleshooting & Errors](docs/6-troubleshooting.md)**
Learn how to read error messages and fix common issues if your changes don't appear.

---

## ℹ️ About This Website

This website serves as the central hub for the **Arbeitsgruppe (AG) Computational Arithmetic Geometry** led by Prof. Dr. Gebhard Böckle at the Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University.

### Research Focus
Our group focuses on:
- Galois representations and their connections to modular forms and elliptic curves
- Deformation theory of Galois representations
- L-functions and Drinfeld modular forms in function field arithmetic
- Computational methods in number theory and arithmetic geometry

### Group Information
- **Location**: Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University
- **Contact**: arithgeo@iwr.uni-heidelberg.de
- **Led by**: Prof. Dr. Gebhard Böckle

---

## 🛠️ Technical Setup

This website is built with **Jekyll** and hosted on **GitHub Pages**.

### Prerequisites
- **Ruby 3.3** (with Bundler; matches CI)
- **Node.js 20+**
- **Python 3** (for validation tooling)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies:**
   ```bash
   bundle install
   npm ci
   python3 -m venv .venv
   .venv/bin/pip install -r requirements-dev.txt
   ```

3. **Start the local server:**
   ```bash
   bundle exec jekyll serve
   ```
   The site will be available at `http://localhost:4000`.

4. **Run the same checks used in CI:**
   ```bash
   bundle exec rake check
   ```

### Maintenance Scripts

We have utility scripts in `scripts/` to maintain data quality. Their dependencies
are pinned in `requirements-dev.txt`.

- **Validation**: `python3 scripts/validate.py` - "The Guardian". Checks data integrity, filenames, and image sizes.
- **Generated-site check**: `python3 scripts/check_generated_site.py` - Rejects empty asset and link attributes after a build.
- **Asset inventory**: `bundle exec rake audit:assets` - Reports duplicate, oversized, unreferenced, and mislabeled assets without changing contributor files.

## AI Assistance Disclosure

AI-assisted development tools have been used for parts of this repository's code,
tooling, tests, and documentation. Changes remain subject to human review and the
same validation and testing requirements as other contributions.
