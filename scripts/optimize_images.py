#!/usr/bin/env python3
"""
Image Optimization Script for AG Computational Arithmetic Geometry Website

This script optimizes images for web performance by:
1. Converting to modern formats (WebP)
2. Compressing while maintaining quality
3. Creating responsive image variants
4. Generating optimized versions for different use cases

Usage: python scripts/optimize_images.py [directory]
"""

import os
import sys
from pathlib import Path
from PIL import Image
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

class ImageOptimizer:
    def __init__(self, source_dir="assets/img", output_dir="assets/img/optimized"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Supported image formats
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

        # Optimization settings
        self.quality_settings = {
            'logo': {'quality': 90, 'max_size': (400, 400)},
            'profile': {'quality': 85, 'max_size': (300, 300)},
            'hero': {'quality': 80, 'max_size': (1920, 1080)},
            'default': {'quality': 85, 'max_size': (1200, 800)}
        }

    def get_image_type(self, filename):
        """Determine image type based on filename patterns"""
        filename_lower = filename.lower()

        if any(keyword in filename_lower for keyword in ['logo', 'brand', 'header']):
            return 'logo'
        elif any(keyword in filename_lower for keyword in ['profile', 'member', 'team']):
            return 'profile'
        elif any(keyword in filename_lower for keyword in ['hero', 'banner', 'background']):
            return 'hero'
        else:
            return 'default'

    def optimize_image(self, input_path, output_path, image_type='default'):
        """Optimize a single image"""
        settings = self.quality_settings.get(image_type, self.quality_settings['default'])

        try:
            # Open and optimize image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img, mask=img.split()[-1])
                    img = background

                # Resize if larger than max dimensions
                if img.size[0] > settings['max_size'][0] or img.size[1] > settings['max_size'][1]:
                    img.thumbnail(settings['max_size'], Image.Resampling.LANCZOS)

                # Save optimized PNG
                png_path = output_path.with_suffix('.png')
                img.save(png_path, 'PNG', optimize=True, quality=settings['quality'])
                original_size = input_path.stat().st_size
                optimized_size = png_path.stat().st_size

                # Convert to WebP if significantly smaller
                webp_path = output_path.with_suffix('.webp')
                img.save(webp_path, 'WebP', quality=settings['quality'], method=6)
                webp_size = webp_path.stat().st_size

                # Keep the smaller format
                if webp_size < optimized_size * 0.9:  # WebP is at least 10% smaller
                    os.remove(png_path)
                    final_path = webp_path
                    final_size = webp_size
                    format_used = 'WebP'
                else:
                    os.remove(webp_path)
                    final_path = png_path
                    final_size = optimized_size
                    format_used = 'PNG'

                # Calculate savings
                savings = original_size - final_size
                savings_percent = (savings / original_size) * 100 if original_size > 0 else 0

                return {
                    'input': input_path,
                    'output': final_path,
                    'original_size': original_size,
                    'optimized_size': final_size,
                    'savings': savings,
                    'savings_percent': savings_percent,
                    'format': format_used,
                    'dimensions': img.size
                }

        except Exception as e:
            print(f"Error optimizing {input_path}: {e}")
            return None

    def process_directory(self):
        """Process all images in the source directory"""
        images = []
        for ext in self.image_extensions:
            images.extend(self.source_dir.glob(f"**/*{ext}"))

        print(f"Found {len(images)} images to process")

        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_image = {
                executor.submit(self.optimize_image, img_path, self.output_dir / f"{img_path.stem}_optimized", self.get_image_type(img_path.name)): img_path
                for img_path in images
            }

            for future in as_completed(future_to_image):
                result = future.result()
                if result:
                    results.append(result)
                    print(f"✓ Optimized: {result['input'].name}")
                    print(f"  Size: {result['original_size']:,} → {result['optimized_size']:,} bytes ({result['savings_percent']:.1f}% savings)")
                    print(f"  Format: {result['format']}, Dimensions: {result['dimensions']}")
                    print()

        # Print summary
        total_original = sum(r['original_size'] for r in results)
        total_optimized = sum(r['optimized_size'] for r in results)
        total_savings = total_original - total_optimized
        avg_savings_percent = (total_savings / total_original) * 100 if total_original > 0 else 0

        print("=" * 50)
        print("OPTIMIZATION COMPLETE")
        print("=" * 50)
        print(f"Images processed: {len(results)}")
        print(f"Total original size: {total_original:,} bytes")
        print(f"Total optimized size: {total_optimized:,} bytes")
        print(f"Total savings: {total_savings:,} bytes ({avg_savings_percent:.1f}%)")
        print(f"Optimized images saved to: {self.output_dir}/")

def main():
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    else:
        source_dir = "assets/img"

    optimizer = ImageOptimizer(source_dir)
    optimizer.process_directory()

if __name__ == "__main__":
    main()