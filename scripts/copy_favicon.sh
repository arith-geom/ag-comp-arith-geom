#!/bin/bash

# Copy favicon to _site directory for proper serving
# This script ensures the favicon is available at the root URL

echo "📄 Copying favicon to _site directory..."

# Copy favicon.ico to _site root
if [ -f "assets/img/favicon.ico" ]; then
    cp assets/img/favicon.ico _site/favicon.ico
    echo "✅ favicon.ico copied to _site/"
else
    echo "⚠️  favicon.ico not found in assets/img/"
fi

# Copy favicon.svg to _site root as well
if [ -f "assets/img/favicon.svg" ]; then
    cp assets/img/favicon.svg _site/favicon.svg
    echo "✅ favicon.svg copied to _site/"
else
    echo "⚠️  favicon.svg not found in assets/img/"
fi

echo "🎉 Favicon setup complete!" 