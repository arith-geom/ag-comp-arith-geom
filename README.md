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

### Prerequisites

**Install Ruby:**
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install ruby-full

# On macOS (using Homebrew)
brew install ruby

# On Windows (using RubyInstaller)
# Download from https://rubyinstaller.org/
```

**Install Git:**
```bash
# On Ubuntu/Debian
sudo apt install git

# On macOS (using Homebrew)
brew install git

# On Windows
# Download from https://git-scm.com/
```

**Install Bundler:**
```bash
gem install bundler
```

### Development Setup

1. **Install dependencies:**
   ```bash
   bundle install
   ```

2. **Start the development server:**
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