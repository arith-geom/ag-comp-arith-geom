#!/bin/bash

# Jekyll Start Script for AG Computational Arithmetic Geometry
# This script starts Jekyll with optimized settings to avoid common issues

echo "🚀 Starting Jekyll for AG Computational Arithmetic Geometry..."
echo "📁 Working directory: $(pwd)"
echo ""

# Check if we're in the right directory
if [ ! -f "_config.yml" ]; then
    echo "❌ Error: _config.yml not found. Please run this script from the project root."
    exit 1
fi

# Clean up any existing cache
echo "🧹 Cleaning up cache files..."
rm -rf .sass-cache/
rm -rf .jekyll-cache/
rm -rf _site/

# Check if search-data.json exists and is causing issues
if [ -f "assets/search-data.json" ]; then
    echo "📄 Found search-data.json - this might cause regeneration loops"
    echo "   Consider excluding it from file watching"
fi

echo ""
echo "🔧 Starting Jekyll with optimized settings..."
echo "   - No incremental build (prevents loops)"
echo "   - No file watching (prevents loops)"
echo "   - Clean cache (prevents SCSS issues)"
echo ""

# Start Jekyll with specific settings to avoid issues
# Note: "--no-incremental" is not a valid flag. We simply omit "--incremental".
bundle exec jekyll serve \
    --host 0.0.0.0 \
    --port 4000 \
    --no-watch \
    --verbose

# Capture exit status to avoid continuing on failure
JEKYLL_STATUS=$?
if [ $JEKYLL_STATUS -ne 0 ]; then
  echo "❌ Jekyll failed to start (exit code $JEKYLL_STATUS). Aborting post-start steps."
  exit $JEKYLL_STATUS
fi

# Copy favicon to _site directory
echo ""
echo "📄 Setting up favicon..."
./scripts/copy_favicon.sh || true

echo ""
echo "✅ Jekyll started successfully!"
echo "🌐 Your site should be available at: http://localhost:4000"
echo ""
echo "💡 Tips:"
echo "   - Press Ctrl+C to stop the server"
echo "   - If you see SCSS errors, try running: bundle update"
echo "   - If you see regeneration loops, check the exclude list in _config.yml" 