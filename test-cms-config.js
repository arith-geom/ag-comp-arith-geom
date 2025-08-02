#!/usr/bin/env node

/**
 * Test script to verify Pages CMS configuration
 * Run with: node test-cms-config.js
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

console.log('🔍 Testing Pages CMS Configuration...\n');

// Test 1: Check if .pages.yml exists and is valid YAML
console.log('1. Checking .pages.yml file...');
try {
  const pagesConfigPath = path.join(__dirname, '.pages.yml');
  const pagesConfigContent = fs.readFileSync(pagesConfigPath, 'utf8');
  const pagesConfig = yaml.load(pagesConfigContent);
  console.log('✅ .pages.yml exists and is valid YAML');
} catch (error) {
  console.log('❌ Error reading .pages.yml:', error.message);
  process.exit(1);
}

// Test 2: Check if required directories exist
console.log('\n2. Checking content directories...');
const requiredDirs = [
  '_members',
  '_publications', 
  '_teaching',
  '_research',
  '_news',
  '_links',
  'assets/img'
];

let allDirsExist = true;
requiredDirs.forEach(dir => {
  const dirPath = path.join(__dirname, dir);
  if (fs.existsSync(dirPath)) {
    console.log(`✅ ${dir}/ exists`);
  } else {
    console.log(`❌ ${dir}/ missing`);
    allDirsExist = false;
  }
});

if (!allDirsExist) {
  console.log('\n⚠️  Some directories are missing. Please create them.');
}

// Test 3: Check if content files exist
console.log('\n3. Checking content files...');
const contentChecks = [
  { dir: '_members', pattern: '.md', minFiles: 1 },
  { dir: '_publications', pattern: '.md', minFiles: 1 },
  { dir: '_teaching', pattern: '.md', minFiles: 1 },
  { dir: '_research', pattern: '.md', minFiles: 1 },
  { dir: '_news', pattern: '.md', minFiles: 1 },
  { dir: '_links', pattern: '.md', minFiles: 1 }
];

contentChecks.forEach(check => {
  const dirPath = path.join(__dirname, check.dir);
  if (fs.existsSync(dirPath)) {
    const files = fs.readdirSync(dirPath).filter(file => file.endsWith(check.pattern));
    if (files.length >= check.minFiles) {
      console.log(`✅ ${check.dir}/ has ${files.length} files`);
    } else {
      console.log(`⚠️  ${check.dir}/ has only ${files.length} files (expected at least ${check.minFiles})`);
    }
  }
});

// Test 4: Check JavaScript integration
console.log('\n4. Checking JavaScript integration...');
const jsFiles = [
  'assets/js/pagescms-integration.js'
];

jsFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file} exists`);
  } else {
    console.log(`❌ ${file} missing`);
  }
});

// Test 5: Check Liquid templates
console.log('\n5. Checking Liquid templates...');
const liquidFiles = [
  '_includes/pagescms-admin.liquid'
];

liquidFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file} exists`);
  } else {
    console.log(`❌ ${file} missing`);
  }
});

// Test 6: Check meta tags in head
console.log('\n6. Checking meta tags...');
const headPath = path.join(__dirname, '_includes/head.liquid');
if (fs.existsSync(headPath)) {
  const headContent = fs.readFileSync(headPath, 'utf8');
  if (headContent.includes('repository-url') && headContent.includes('repository-branch')) {
    console.log('✅ Repository meta tags found in head.liquid');
  } else {
    console.log('⚠️  Repository meta tags missing from head.liquid');
  }
} else {
  console.log('❌ head.liquid not found');
}

console.log('\n🎉 CMS Configuration Test Complete!');
console.log('\nNext steps:');
console.log('1. Visit https://app.pagescms.org/');
console.log('2. Sign in with your GitHub account');
console.log('3. Select your repository: hiwiwebsiteaddingnewstuff');
console.log('4. Select branch: main');
console.log('5. Start managing your content!');

console.log('\n📚 Documentation: https://pagescms.org/docs/');
console.log('🔧 Configuration Guide: https://pagescms.org/docs/configuration/'); 