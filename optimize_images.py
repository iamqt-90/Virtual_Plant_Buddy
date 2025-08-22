#!/usr/bin/env python3
"""
Image optimization script for Virtual Plant Buddy
Reduces file sizes while maintaining quality
"""

from PIL import Image
import os
import sys

def optimize_image(input_path, output_path=None, quality=85, max_size=(400, 400)):
    """
    Optimize an image by reducing size and quality
    
    Args:
        input_path: Path to input image
        output_path: Path for output (optional, overwrites input if None)
        quality: JPEG quality (1-100, higher = better quality)
        max_size: Maximum dimensions (width, height)
    """
    try:
        # Open image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for JPEG)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Set output path
            if output_path is None:
                output_path = input_path
            
            # Save optimized image
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get file sizes
            original_size = os.path.getsize(input_path) if input_path != output_path else 0
            new_size = os.path.getsize(output_path)
            
            print(f"✅ Optimized: {os.path.basename(output_path)}")
            if original_size > 0:
                reduction = ((original_size - new_size) / original_size) * 100
                print(f"   Size: {original_size:,} → {new_size:,} bytes ({reduction:.1f}% reduction)")
            else:
                print(f"   Size: {new_size:,} bytes")
            
    except Exception as e:
        print(f"❌ Error optimizing {input_path}: {e}")

def optimize_folder(folder_path, extensions=('.png', '.jpg', '.jpeg', '.webp')):
    """Optimize all images in a folder"""
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
    
    print(f"🔍 Scanning folder: {folder_path}")
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(extensions):
            file_path = os.path.join(folder_path, filename)
            optimize_image(file_path)

if __name__ == "__main__":
    # Check if assets folder exists
    assets_folder = "assets/images"
    
    if os.path.exists(assets_folder):
        print("🌱 Virtual Plant Buddy - Image Optimizer")
        print("=" * 40)
        optimize_folder(assets_folder)
        print("\n✨ Optimization complete!")
    else:
        print(f"📁 Assets folder not found: {assets_folder}")
        print("💡 Place your plant images in: assets/images/")
        print("   Expected files:")
        print("   - seed.png.webp")
        print("   - sprout.png.webp") 
        print("   - flower.png.webp")