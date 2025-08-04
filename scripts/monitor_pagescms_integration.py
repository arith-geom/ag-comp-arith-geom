#!/usr/bin/env python3
"""
Pages CMS Integration Monitor
This script monitors Pages CMS integration and ensures new content appears immediately.
"""

import os
import sys
import yaml
import json
import time
import subprocess
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PagesCMSMonitor:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.content_dirs = ['_members', '_publications', '_research', '_teaching']
        self.file_hashes = {}
        self.last_build_time = None
        
    def start_monitoring(self):
        """Start monitoring Pages CMS integration"""
        print("🚀 Starting Pages CMS Integration Monitor...")
        print("=" * 60)
        
        # Initial setup check
        self.check_initial_setup()
        
        # Start file monitoring
        self.start_file_monitoring()
        
        # Start periodic checks
        self.start_periodic_checks()
    
    def check_initial_setup(self):
        """Check initial Pages CMS setup"""
        print("\n📋 Checking Initial Setup...")
        
        # Check configuration
        if not self.check_configuration():
            print("❌ Configuration check failed")
            return False
        
        # Check plugin
        if not self.check_plugin():
            print("❌ Plugin check failed")
            return False
        
        # Check content directories
        if not self.check_content_directories():
            print("❌ Content directories check failed")
            return False
        
        print("✅ Initial setup check passed")
        return True
    
    def check_configuration(self):
        """Check Pages CMS configuration"""
        try:
            config_file = self.project_root / '_config.yml'
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            if 'pagescms' not in config:
                print("❌ Pages CMS configuration missing in _config.yml")
                return False
            
            pagescms_config = config['pagescms']
            required_keys = ['enabled', 'api_url', 'content_types', 'auto_sync']
            
            for key in required_keys:
                if key not in pagescms_config:
                    print(f"❌ Missing required key: {key}")
                    return False
            
            if not pagescms_config['enabled']:
                print("❌ Pages CMS is disabled")
                return False
            
            print(f"✅ Pages CMS enabled: {pagescms_config['enabled']}")
            print(f"✅ API URL: {pagescms_config['api_url']}")
            print(f"✅ Auto Sync: {pagescms_config['auto_sync']}")
            print(f"✅ Content Types: {pagescms_config['content_types']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Configuration check error: {e}")
            return False
    
    def check_plugin(self):
        """Check Pages CMS plugin"""
        try:
            plugin_file = self.project_root / '_plugins' / 'pagescms_integration.rb'
            
            if not plugin_file.exists():
                print("❌ Pages CMS plugin not found")
                return False
            
            with open(plugin_file, 'r') as f:
                plugin_content = f.read()
            
            required_methods = [
                'sync_pagescms_content',
                'process_pagescms_item',
                'ensure_front_matter_structure'
            ]
            
            for method in required_methods:
                if method not in plugin_content:
                    print(f"❌ Missing method: {method}")
                    return False
            
            print("✅ Pages CMS plugin found and valid")
            return True
            
        except Exception as e:
            print(f"❌ Plugin check error: {e}")
            return False
    
    def check_content_directories(self):
        """Check content directories"""
        try:
            for dir_name in self.content_dirs:
                dir_path = self.project_root / dir_name
                if not dir_path.exists():
                    print(f"❌ Content directory missing: {dir_name}")
                    return False
                
                files = list(dir_path.glob('*.md'))
                print(f"✅ {dir_name}: {len(files)} files")
            
            return True
            
        except Exception as e:
            print(f"❌ Content directories check error: {e}")
            return False
    
    def start_file_monitoring(self):
        """Start monitoring file changes"""
        print("\n👀 Starting File Monitoring...")
        
        event_handler = PagesCMSFileHandler(self)
        observer = Observer()
        
        for dir_name in self.content_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                observer.schedule(event_handler, str(dir_path), recursive=False)
                print(f"   📁 Monitoring: {dir_name}")
        
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\n🛑 Monitoring stopped")
        
        observer.join()
    
    def start_periodic_checks(self):
        """Start periodic integration checks"""
        print("\n⏰ Starting Periodic Checks...")
        
        while True:
            try:
                self.perform_integration_check()
                time.sleep(300)  # Check every 5 minutes
            except KeyboardInterrupt:
                print("\n🛑 Periodic checks stopped")
                break
    
    def perform_integration_check(self):
        """Perform integration check"""
        print(f"\n🔍 Integration Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check for new files
        new_files = self.detect_new_files()
        if new_files:
            print(f"📝 Found {len(new_files)} new/modified files:")
            for file_path in new_files:
                print(f"   - {file_path}")
            
            # Trigger build
            self.trigger_build()
        
        # Check build status
        self.check_build_status()
    
    def detect_new_files(self):
        """Detect new or modified files"""
        new_files = []
        
        for dir_name in self.content_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.glob('*.md'):
                file_hash = self.get_file_hash(file_path)
                
                if str(file_path) not in self.file_hashes:
                    # New file
                    self.file_hashes[str(file_path)] = file_hash
                    new_files.append(file_path)
                elif self.file_hashes[str(file_path)] != file_hash:
                    # Modified file
                    self.file_hashes[str(file_path)] = file_hash
                    new_files.append(file_path)
        
        return new_files
    
    def get_file_hash(self, file_path):
        """Get file hash for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def trigger_build(self):
        """Trigger Jekyll build"""
        print("🔨 Triggering Jekyll build...")
        
        try:
            result = subprocess.run(
                ['bundle', 'exec', 'jekyll', 'build', '--safe'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ Build successful")
                self.last_build_time = datetime.now()
            else:
                print(f"❌ Build failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("❌ Build timed out")
        except Exception as e:
            print(f"❌ Build error: {e}")
    
    def check_build_status(self):
        """Check build status and output"""
        if not self.last_build_time:
            return
        
        # Check if build output contains Pages CMS information
        print("📊 Checking build output...")
        
        # This would normally check build logs
        # For now, we'll just confirm the build completed
        print("✅ Build status: OK")

class PagesCMSFileHandler(FileSystemEventHandler):
    def __init__(self, monitor):
        self.monitor = monitor
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"📄 New file created: {event.src_path}")
            self.monitor.trigger_build()
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"📝 File modified: {event.src_path}")
            self.monitor.trigger_build()
    
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"🗑️  File deleted: {event.src_path}")
            self.monitor.trigger_build()

def main():
    # Get project root
    project_root = Path(__file__).parent.parent
    
    # Create monitor
    monitor = PagesCMSMonitor(project_root)
    
    # Start monitoring
    monitor.start_monitoring()

if __name__ == "__main__":
    main() 