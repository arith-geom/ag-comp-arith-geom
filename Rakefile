# frozen_string_literal: true

require "rake"

python = ENV.fetch("PYTHON", File.executable?(".venv/bin/python") ? ".venv/bin/python" : "python3")

desc "Validate CMS data and uploaded assets"
task :validate do
  sh "#{python} scripts/validate.py"
end

namespace :lint do
  desc "Lint YAML configuration and data"
  task :yaml do
    sh "#{python} -m yamllint ."
  end

  desc "Lint SCSS sources"
  task :styles do
    sh "npm run lint:styles"
  end
end

namespace :audit do
  desc "Report duplicate, oversized, unreferenced, and mislabeled assets"
  task :assets do
    sh "#{python} scripts/audit_assets.py"
  end
end

desc "Build the Jekyll site"
task :build do
  sh "bundle exec jekyll build"
end

desc "Run unit tests for custom validators and Jekyll plugins"
task :test do
  sh "#{python} scripts/test_validate.py"
  sh "bundle exec ruby scripts/test_plugins.rb"
end

desc "Check generated HTML and internal links"
task site: :build do
  sh "bundle exec htmlproofer ./_site --disable-external --allow-hash-href " \
     "--swap-urls '/ag-comp-arith-geom/:/' --no-check-internal-hash --no-enforce-https"
  sh "#{python} scripts/check_generated_site.py"
  sh "#{python} scripts/check_external_resources.py"
  sh "#{python} scripts/check_seo.py"
  sh "#{python} scripts/check_performance.py"
end

desc "Run all repository checks"
task check: [:validate, "lint:yaml", "lint:styles", :test, :site, "audit:assets"] do
  sh "npm run audit"
end

task default: :check
