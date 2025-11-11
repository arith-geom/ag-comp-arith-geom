#!/bin/bash
#
# Setup script for the Jekyll project.
#
# This script installs the required dependencies for the project, including
# Ruby and Node.js packages. It also sets up the vendor assets.
#
# Usage:
#   ./scripts/setup.sh
#

# Exit immediately if a command exits with a non-zero status.
set -e

# Print a message to the console.
function message() {
  echo "-----> $1"
}

# Install Ruby dependencies.
message "Installing Ruby dependencies..."
gem install bundler
bundle install

# Install Node.js dependencies.
message "Installing Node.js dependencies..."
npm install

# Install vendor assets.
message "Installing vendor assets..."
bundle exec rake vendor

message "Setup complete."