#!/usr/bin/env python3
"""
Image Optimization Script for Pages CMS
Optimizes large images for better website performance
"""

import os
import sys
from PIL import Image
import argparse

def optimize_image(input_path, output_path=None, max_size=(800, 800), quality=85):
    """Optimize a single image"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if larger than max_size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            if output_path is None:
                output_path = input_path
            
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            optimized_size = os.path.getsize(output_path)
            savings = ((original_size - optimized_size) / original_size) * 100
            
            print(f"✓ Optimized {input_path}")
            print(f"  Original: {original_size:,} bytes")
            print(f"  Optimized: {optimized_size:,} bytes")
            print(f"  Savings: {savings:.1f}%")
            
            return True
            
    except Exception as e:
        print(f"✗ Error optimizing {input_path}: {e}")
        return False

def find_large_images(directory, min_size_mb=0.5):
    """Find large images in directory"""
    large_images = []
    min_size_bytes = min_size_mb * 1024 * 1024
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    if size > min_size_bytes:
                        large_images.append((file_path, size))
                except Exception:
                    pass
    
    return sorted(large_images, key=lambda x: x[1], reverse=True)

def main():
    parser = argparse.ArgumentParser(description='Optimize images for Pages CMS')
    parser.add_argument('--directory', default='assets/img', help='Directory to scan for images')
    parser.add_argument('--max-size', default='800x800', help='Maximum image dimensions (WxH)')
    parser.add_argument('--quality', type=int, default=85, help='JPEG quality (1-100)')
    parser.add_argument('--min-size-mb', type=float, default=0.5, help='Minimum file size to optimize (MB)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be optimized without making changes')
    
    args = parser.parse_args()
    
    # Parse max size
    try:
        max_width, max_height = map(int, args.max_size.split('x'))
        max_size = (max_width, max_height)
    except ValueError:
        print("Error: max-size must be in format WxH (e.g., 800x800)")
        sys.exit(1)
    
    print(f"🔍 Scanning for large images in {args.directory}...")
    print(f"📏 Max size: {max_size[0]}x{max_size[1]} pixels")
    print(f"🎯 Quality: {args.quality}%")
    print(f"📦 Min size: {args.min_size_mb}MB")
    
    if not os.path.exists(args.directory):
        print(f"❌ Directory {args.directory} not found")
        sys.exit(1)
    
    large_images = find_large_images(args.directory, args.min_size_mb)
    
    if not large_images:
        print("✅ No large images found!")
        return
    
    print(f"\n📊 Found {len(large_images)} large images:")
    total_original_size = 0
    
    for file_path, size in large_images:
        size_mb = size / (1024 * 1024)
        print(f"  • {file_path} ({size_mb:.1f}MB)")
        total_original_size += size
    
    print(f"\n📈 Total size: {total_original_size / (1024 * 1024):.1f}MB")
    
    if args.dry_run:
        print("\n🔍 DRY RUN - No changes will be made")
        return
    
    print(f"\n⚡ Starting optimization...")
    
    success_count = 0
    total_savings = 0
    
    for file_path, original_size in large_images:
        if optimize_image(file_path, max_size=max_size, quality=args.quality):
            success_count += 1
            optimized_size = os.path.getsize(file_path)
            total_savings += (original_size - optimized_size)
    
    print(f"\n🎉 Optimization complete!")
    print(f"✅ Successfully optimized: {success_count}/{len(large_images)} images")
    print(f"💾 Total space saved: {total_savings / (1024 * 1024):.1f}MB")
    
    if success_count > 0:
        print(f"📊 Average savings: {(total_savings / success_count) / (1024 * 1024):.1f}MB per image")

if __name__ == "__main__":
    main() 