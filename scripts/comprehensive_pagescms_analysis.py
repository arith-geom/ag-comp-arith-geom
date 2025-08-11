#!/usr/bin/env python3
"""
Comprehensive Pages CMS Analysis Script
Deep analysis of Pages CMS configuration, content structure, and logical consistency
"""

import os
import json
import yaml
import sys
import re
from pathlib import Path
from collections import defaultdict

class PagesCMSAnalyzer:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.issues = []
        self.warnings = []
        self.recommendations = []
        self.stats = defaultdict(int)
        
    def analyze(self):
        """Run comprehensive analysis"""
        print("=" * 80)
        print("COMPREHENSIVE PAGES CMS ANALYSIS")
        print("=" * 80)
        
        # Run all analysis modules
        self.analyze_configuration_files()
        self.analyze_content_structure()
        self.analyze_field_mapping()
        self.analyze_file_naming()
        self.analyze_validation_rules()
        self.analyze_references()
        self.analyze_performance()
        self.analyze_security()
        self.analyze_content_consistency()
        self.analyze_integration_logic()
        
        # Generate comprehensive report
        self.generate_report()
        
    def analyze_configuration_files(self):
        """Analyze configuration files for issues"""
        print("\n🔍 Analyzing Configuration Files...")
        
        # Check .pages.yml
        try:
            with open('.pages.yml', 'r', encoding='utf-8') as f:
                pages_config = yaml.safe_load(f)
            
            # Check for required sections
            required_sections = ['media', 'content']
            for section in required_sections:
                if section not in pages_config:
                    self.issues.append(f"Missing required section '{section}' in .pages.yml")
                else:
                    self.stats[f"config_sections_{section}"] = 1
            
            # Check content types
            content_types = pages_config.get('content', [])
            self.stats['content_types'] = len(content_types)
            
            # Check for duplicate content type names
            content_names = [ct.get('name') for ct in content_types if ct.get('name')]
            duplicates = [name for name in set(content_names) if content_names.count(name) > 1]
            if duplicates:
                self.issues.append(f"Duplicate content type names: {duplicates}")
            
            # Check field definitions
            for content_type in content_types:
                self.analyze_content_type_fields(content_type)
                
        except Exception as e:
            self.issues.append(f"Error reading .pages.yml: {e}")
    
    def analyze_content_type_fields(self, content_type):
        """Analyze fields within a content type"""
        content_name = content_type.get('name', 'unknown')
        fields = content_type.get('fields', [])
        
        # Check for required fields
        required_fields = []
        for field in fields:
            if field.get('required'):
                required_fields.append(field.get('name'))
        
        # Check for field type consistency
        field_types = {}
        for field in fields:
            field_name = field.get('name')
            field_type = field.get('type')
            if field_name and field_type:
                if field_name in field_types and field_types[field_name] != field_type:
                    self.warnings.append(f"Inconsistent field type for '{field_name}' in {content_name}")
                field_types[field_name] = field_type
        
        # Check for validation rules
        for field in fields:
            self.analyze_field_validation(field, content_name)
    
    def analyze_field_validation(self, field, content_name):
        """Analyze field validation rules"""
        field_name = field.get('name', 'unknown')
        validation = field.get('validation', {})
        
        # Check pattern validation
        pattern = validation.get('pattern')
        if pattern:
            try:
                re.compile(pattern)
            except re.error:
                self.issues.append(f"Invalid regex pattern for field '{field_name}' in {content_name}: {pattern}")
        
        # Check length validation
        min_length = validation.get('min_length')
        max_length = validation.get('max_length')
        if min_length and max_length and min_length > max_length:
            self.issues.append(f"Invalid length validation for field '{field_name}' in {content_name}: min > max")
    
    def analyze_content_structure(self):
        """Analyze content directory structure"""
        print("\n📁 Analyzing Content Structure...")
        
        content_dirs = {
            '_members': 'members',
            '_publications': 'publications', 
            '_research': 'research',
            '_teaching': 'teaching'
        }
        
        for dir_path, content_type in content_dirs.items():
            if not os.path.exists(dir_path):
                self.issues.append(f"Content directory '{dir_path}' not found")
                continue
            
            # Count files
            md_files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
            self.stats[f'{content_type}_files'] = len(md_files)
            
            # Check file structure
            for file_name in md_files[:5]:  # Sample first 5 files
                file_path = os.path.join(dir_path, file_name)
                self.analyze_content_file(file_path, content_type)
    
    def analyze_content_file(self, file_path, content_type):
        """Analyze individual content file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check front matter
            if not content.startswith('---'):
                self.warnings.append(f"Missing front matter in {file_path}")
                return
            
            # Parse front matter
            parts = content.split('---', 3)
            if len(parts) < 3:
                self.warnings.append(f"Invalid front matter structure in {file_path}")
                return
            
            front_matter = yaml.safe_load(parts[1])
            if not front_matter:
                self.warnings.append(f"Empty front matter in {file_path}")
                return
            
            # Check required fields based on content type
            self.check_required_fields(front_matter, content_type, file_path)
            
        except Exception as e:
            self.warnings.append(f"Error reading {file_path}: {e}")
    
    def check_required_fields(self, front_matter, content_type, file_path):
        """Check if required fields are present"""
        required_fields_map = {
            'members': ['name', 'role', 'status'],
            'publications': ['title', 'authors', 'year'],
            'research': ['title', 'description'],
            'teaching': ['title', 'semester']
        }
        
        required_fields = required_fields_map.get(content_type, [])
        missing_fields = [field for field in required_fields if field not in front_matter]
        
        if missing_fields:
            self.warnings.append(f"Missing required fields in {file_path}: {missing_fields}")
    
    def analyze_field_mapping(self):
        """Analyze field mapping between config and actual content"""
        print("\n🔗 Analyzing Field Mapping...")
        
        # Load configuration
        try:
            with open('.pages.yml', 'r', encoding='utf-8') as f:
                pages_config = yaml.safe_load(f)
            
            content_types = pages_config.get('content', [])
            
            for content_type in content_types:
                content_name = content_type.get('name')
                fields = content_type.get('fields', [])
                field_names = [f.get('name') for f in fields if f.get('name')]
                
                # Check if fields are used in actual content
                self.check_field_usage(content_name, field_names)
                
        except Exception as e:
            self.issues.append(f"Error analyzing field mapping: {e}")
    
    def check_field_usage(self, content_name, field_names):
        """Check if configured fields are actually used in content"""
        dir_mapping = {
            'members': '_members',
            'publications': '_publications',
            'research': '_research',
            'teaching': '_teaching'
        }
        
        dir_path = dir_mapping.get(content_name)
        if not dir_path or not os.path.exists(dir_path):
            return
        
        # Sample a few files to check field usage
        md_files = [f for f in os.listdir(dir_path) if f.endswith('.md')][:3]
        
        for file_name in md_files:
            file_path = os.path.join(dir_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                parts = content.split('---', 3)
                if len(parts) >= 3:
                    front_matter = yaml.safe_load(parts[1])
                    if front_matter:
                        used_fields = set(front_matter.keys())
                        unused_fields = set(field_names) - used_fields
                        if unused_fields:
                            self.recommendations.append(f"Unused fields in {content_name}: {unused_fields}")
                            
            except Exception as e:
                self.warnings.append(f"Error checking field usage in {file_path}: {e}")
    
    def analyze_file_naming(self):
        """Analyze file naming conventions"""
        print("\n📝 Analyzing File Naming...")
        
        # Check for consistent naming patterns
        content_dirs = ['_members', '_publications', '_research', '_teaching']
        
        for dir_path in content_dirs:
            if not os.path.exists(dir_path):
                continue
            
            files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
            
            # Check for naming patterns
            patterns = {
                'kebab-case': r'^[a-z0-9]+(-[a-z0-9]+)*\.md$',
                'snake_case': r'^[a-z0-9]+(_[a-z0-9]+)*\.md$',
                'camelCase': r'^[a-z]+([A-Z][a-z0-9]+)*\.md$'
            }
            
            pattern_counts = defaultdict(int)
            for file_name in files:
                for pattern_name, pattern in patterns.items():
                    if re.match(pattern, file_name):
                        pattern_counts[pattern_name] += 1
                        break
            
            # Check for consistency
            if len(pattern_counts) > 1:
                self.warnings.append(f"Mixed naming patterns in {dir_path}: {dict(pattern_counts)}")
            
            # Check for special characters
            problematic_files = []
            for file_name in files:
                if re.search(r'[^a-zA-Z0-9\-_\.]', file_name):
                    problematic_files.append(file_name)
            
            if problematic_files:
                self.issues.append(f"Files with special characters in {dir_path}: {problematic_files}")
    
    def analyze_validation_rules(self):
        """Analyze validation rules for consistency"""
        print("\n✅ Analyzing Validation Rules...")
        
        try:
            with open('.pages.yml', 'r', encoding='utf-8') as f:
                pages_config = yaml.safe_load(f)
            
            content_types = pages_config.get('content', [])
            
            for content_type in content_types:
                fields = content_type.get('fields', [])
                
                for field in fields:
                    validation = field.get('validation', {})
                    
                    # Check email validation consistency
                    if field.get('name') == 'email':
                        pattern = validation.get('pattern', '')
                        if pattern and 'email' not in pattern.lower():
                            self.warnings.append(f"Inconsistent email validation pattern: {pattern}")
                    
                    # Check URL validation consistency
                    if field.get('name') in ['website', 'url']:
                        pattern = validation.get('pattern', '')
                        if pattern and not pattern.startswith('^https?://'):
                            self.warnings.append(f"Inconsistent URL validation pattern: {pattern}")
                    
                    # Check length validation
                    min_length = validation.get('min_length')
                    max_length = validation.get('max_length')
                    if min_length and max_length:
                        if min_length > max_length:
                            self.issues.append(f"Invalid length validation: min({min_length}) > max({max_length})")
                        elif max_length - min_length < 5:
                            self.recommendations.append(f"Very restrictive length validation: {min_length}-{max_length}")
            
        except Exception as e:
            self.issues.append(f"Error analyzing validation rules: {e}")
    
    def analyze_references(self):
        """Analyze reference fields and their targets"""
        print("\n🔗 Analyzing References...")
        
        try:
            with open('.pages.yml', 'r', encoding='utf-8') as f:
                pages_config = yaml.safe_load(f)
            
            content_types = pages_config.get('content', [])
            
            # Build reference map
            reference_map = {}
            for content_type in content_types:
                content_name = content_type.get('name')
                fields = content_type.get('fields', [])
                
                for field in fields:
                    if field.get('type') == 'reference':
                        target_collection = field.get('collection')
                        if target_collection:
                            if target_collection not in reference_map:
                                reference_map[target_collection] = []
                            reference_map[target_collection].append({
                                'source': content_name,
                                'field': field.get('name')
                            })
            
            # Check if referenced collections exist
            for target_collection, references in reference_map.items():
                target_dir = f"_{target_collection}"
                if not os.path.exists(target_dir):
                    self.issues.append(f"Referenced collection '{target_collection}' not found (referenced by {references})")
                else:
                    self.stats['references'] += len(references)
            
        except Exception as e:
            self.issues.append(f"Error analyzing references: {e}")
    
    def analyze_performance(self):
        """Analyze performance considerations"""
        print("\n⚡ Analyzing Performance...")
        
        # Check file sizes
        content_dirs = ['_members', '_publications', '_research', '_teaching']
        total_size = 0
        
        for dir_path in content_dirs:
            if not os.path.exists(dir_path):
                continue
            
            files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
            for file_name in files:
                file_path = os.path.join(dir_path, file_name)
                try:
                    size = os.path.getsize(file_path)
                    total_size += size
                    if size > 10000:  # 10KB
                        self.warnings.append(f"Large content file: {file_path} ({size} bytes)")
                except Exception:
                    pass
        
        self.stats['total_content_size'] = total_size
        
        # Check for potential performance issues
        if total_size > 1000000:  # 1MB
            self.recommendations.append("Consider optimizing large content files for better performance")
        
        # Check image sizes
        img_dir = 'assets/img'
        if os.path.exists(img_dir):
            img_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            large_images = []
            
            for img_file in img_files:
                img_path = os.path.join(img_dir, img_file)
                try:
                    size = os.path.getsize(img_path)
                    if size > 500000:  # 500KB
                        large_images.append(f"{img_file} ({size} bytes)")
                except Exception:
                    pass
            
            if large_images:
                self.recommendations.append(f"Consider optimizing large images: {large_images[:5]}")
    
    def analyze_security(self):
        """Analyze security considerations"""
        print("\n🔒 Analyzing Security...")
        
        # Check file permissions
        sensitive_files = ['.pages.yml', 'pagescms.config.json', '_config.yml']
        
        for file_name in sensitive_files:
            if os.path.exists(file_name):
                try:
                    mode = oct(os.stat(file_name).st_mode)[-3:]
                    if mode != '644':
                        self.warnings.append(f"Non-standard file permissions for {file_name}: {mode}")
                except Exception:
                    pass
        
        # Check for sensitive information in content
        content_dirs = ['_members', '_publications', '_research', '_teaching']
        
        for dir_path in content_dirs:
            if not os.path.exists(dir_path):
                continue
            
            files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
            for file_name in files[:3]:  # Sample first 3 files
                file_path = os.path.join(dir_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for potential sensitive data
                    sensitive_patterns = [
                        r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',  # ORCID
                        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
                        r'\b\d{3}-\d{3}-\d{4}\b',  # Phone
                    ]
                    
                    for pattern in sensitive_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            self.recommendations.append(f"Potential sensitive data in {file_path}: {matches[:3]}")
                            
                except Exception:
                    pass
    
    def analyze_content_consistency(self):
        """Analyze content consistency across files"""
        print("\n📊 Analyzing Content Consistency...")
        
        # Check for consistent field usage
        content_dirs = ['_members', '_publications', '_research', '_teaching']
        
        for dir_path in content_dirs:
            if not os.path.exists(dir_path):
                continue
            
            files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
            if len(files) < 2:
                continue
            
            # Sample files for consistency check
            sample_files = files[:min(5, len(files))]
            field_usage = defaultdict(int)
            
            for file_name in sample_files:
                file_path = os.path.join(dir_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    parts = content.split('---', 3)
                    if len(parts) >= 3:
                        front_matter = yaml.safe_load(parts[1])
                        if front_matter:
                            for field in front_matter.keys():
                                field_usage[field] += 1
                            
                except Exception:
                    pass
            
            # Check for inconsistent field usage
            total_files = len(sample_files)
            inconsistent_fields = []
            
            for field, count in field_usage.items():
                usage_percentage = (count / total_files) * 100
                if 20 < usage_percentage < 80:  # Neither rare nor common
                    inconsistent_fields.append(field)
            
            if inconsistent_fields:
                self.warnings.append(f"Inconsistent field usage in {dir_path}: {inconsistent_fields}")
    
    def analyze_integration_logic(self):
        """Analyze integration plugin logic"""
        print("\n🔧 Analyzing Integration Logic...")
        
        plugin_path = '_plugins/pagescms_integration.rb'
        if not os.path.exists(plugin_path):
            self.issues.append("Pages CMS integration plugin not found")
            return
        
        try:
            with open(plugin_path, 'r', encoding='utf-8') as f:
                plugin_content = f.read()
            
            # Check for required methods
            required_methods = [
                'setup_pagescms_integration',
                'process_pagescms_content',
                'create_pagescms_config'
            ]
            
            for method in required_methods:
                if method not in plugin_content:
                    self.issues.append(f"Missing required method '{method}' in integration plugin")
            
            # Check for error handling
            if 'rescue' not in plugin_content and 'begin' not in plugin_content:
                self.recommendations.append("Consider adding error handling to integration plugin")
            
            # Check for logging
            if 'Jekyll.logger' not in plugin_content:
                self.recommendations.append("Consider adding logging to integration plugin")
            
        except Exception as e:
            self.issues.append(f"Error analyzing integration plugin: {e}")
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 80)
        
        # Statistics
        print(f"\n📈 STATISTICS:")
        print(f"  • Content Types: {self.stats.get('content_types', 0)}")
        print(f"  • Total Content Files: {sum(self.stats.get(f'{ct}_files', 0) for ct in ['members', 'publications', 'research', 'teaching'])}")
        print(f"  • References: {self.stats.get('references', 0)}")
        print(f"  • Total Content Size: {self.stats.get('total_content_size', 0):,} bytes")
        
        # Issues
        if self.issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        else:
            print(f"\n✅ No critical issues found!")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        else:
            print(f"\n✅ No warnings!")
        
        # Recommendations
        if self.recommendations:
            print(f"\n💡 RECOMMENDATIONS ({len(self.recommendations)}):")
            for i, rec in enumerate(self.recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print(f"\n✅ No recommendations!")
        
        # Overall assessment
        print(f"\n🎯 OVERALL ASSESSMENT:")
        if not self.issues and not self.warnings:
            print("  🎉 EXCELLENT - Pages CMS is well-configured and ready for production!")
        elif not self.issues:
            print("  ✅ GOOD - Minor issues to address, but generally well-configured")
        else:
            print("  ⚠️  NEEDS ATTENTION - Critical issues should be resolved before production use")
        
        print(f"\n📋 NEXT STEPS:")
        if self.issues:
            print("  1. Fix critical issues listed above")
        if self.warnings:
            print("  2. Address warnings for better configuration")
        if self.recommendations:
            print("  3. Consider implementing recommendations for optimization")
        print("  4. Run validation tests after fixes")
        print("  5. Test Pages CMS integration thoroughly")

def main():
    """Main analysis function"""
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    
    print(f"Running comprehensive Pages CMS analysis in: {project_dir}")
    
    analyzer = PagesCMSAnalyzer(project_dir)
    analyzer.analyze()

if __name__ == "__main__":
    main() 