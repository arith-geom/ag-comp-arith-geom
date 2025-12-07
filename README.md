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
- **Ruby** (with Bundler)
- **Python 3** (for maintenance scripts)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies:**
   ```bash
   bundle install
   ```

3. **Start the local server:**
   ```bash
   bundle exec jekyll serve
   ```
   The site will be available at `http://localhost:4000`.

### Maintenance Scripts

We have utility scripts in `scripts/` to maintain data quality. These require `PyYAML`:

```bash
pip install PyYAML
```

- **Validation**: `python3 scripts/validate.py` - "The Guardian". Checks data integrity, filenames, and image sizes.
- **Sorting**: `python3 scripts/sort_data.py` - Enforces consistent ordering.
- **Cleanup**: `python3 scripts/cleanup_unused_media.py` - Finds files not used in content.
