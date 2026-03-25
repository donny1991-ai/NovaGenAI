#!/usr/bin/env python3
"""
Image Optimization Script for NovaGenAI Website
Converts JPG/PNG references to WebP with fallback, adds dimensions, and optimizes loading.
"""

import re
import os
from pathlib import Path

# Image dimension mappings
DIMENSIONS = {
    # Service images (all 1376x768)
    'images/services/': (1376, 768),
    
    # Blog avatars
    'blog/images/don-avatar': (1024, 1024),
    
    # Logo images
    'blog/images/novagenai-logo': (1213, 339),
    'images/novagenai-logo-new': (1213, 339),
    
    # Hero images (1600x914)
    'images/agents-hero': (1600, 914),
    'images/stem-cell-lab-new': (1600, 914),
    'images/team-collab-new': (1600, 914),
    
    # Blog images
    'blog/images/blog-multi-omics': (1200, 675),
}

# Hero/above-fold images (fetchpriority="high")
HERO_IMAGES = [
    'cloud-hero.jpg',
    'erp-hero.jpg',
    'custom-hero.jpg',
    'agents-hero.jpg',
]

def get_dimensions(img_path):
    """Get dimensions for an image based on path matching."""
    for pattern, dims in DIMENSIONS.items():
        if pattern in img_path:
            return dims
    return None

def is_hero_image(img_src):
    """Check if image is a hero/above-fold image."""
    return any(hero in img_src for hero in HERO_IMAGES)

def update_img_tag(match):
    """Update a single <img> tag with WebP, dimensions, and loading attributes."""
    full_tag = match.group(0)
    
    # Extract src attribute
    src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag)
    if not src_match:
        return full_tag
    
    src = src_match.group(1)
    
    # Skip if already WebP
    if src.endswith('.webp'):
        return full_tag
    
    # Skip if not JPG/PNG
    if not (src.endswith('.jpg') or src.endswith('.png') or src.endswith('.jpeg')):
        return full_tag
    
    # Check if WebP version exists
    webp_src = re.sub(r'\.(jpg|png|jpeg)$', '.webp', src)
    webp_path = Path('/root/.openclaw/workspace/novagenai-website') / webp_src
    
    if not webp_path.exists():
        # No WebP version, but still add dimensions if missing
        dims = get_dimensions(src)
        if dims and 'width=' not in full_tag and 'height=' not in full_tag:
            width, height = dims
            full_tag = full_tag.replace('<img', f'<img width="{width}" height="{height}"')
        return full_tag
    
    # Get dimensions
    dims = get_dimensions(src)
    
    # Build new tag
    new_tag = full_tag
    
    # Replace src with WebP
    new_tag = new_tag.replace(src, webp_src)
    
    # Add dimensions if not present
    if dims and 'width=' not in new_tag and 'height=' not in new_tag:
        width, height = dims
        new_tag = new_tag.replace('<img', f'<img width="{width}" height="{height}"')
    
    # Add/update loading attribute
    is_hero = is_hero_image(src)
    
    if 'loading=' in new_tag:
        # Update existing loading attribute
        if is_hero:
            new_tag = re.sub(r'loading=["\']lazy["\']', 'loading="eager"', new_tag)
        else:
            new_tag = re.sub(r'loading=["\']eager["\']', 'loading="lazy"', new_tag)
    else:
        # Add loading attribute
        loading_val = 'eager' if is_hero else 'lazy'
        new_tag = new_tag.replace('<img', f'<img loading="{loading_val}"')
    
    # Add fetchpriority="high" for hero images
    if is_hero and 'fetchpriority=' not in new_tag:
        new_tag = new_tag.replace('<img', '<img fetchpriority="high"')
    
    return new_tag

def process_html_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update all <img> tags
    original = content
    content = re.sub(r'<img[^>]+>', update_img_tag, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all HTML files in the website."""
    root = Path('/root/.openclaw/workspace/novagenai-website')
    html_files = list(root.glob('**/*.html'))
    
    updated = 0
    for html_file in html_files:
        if process_html_file(html_file):
            print(f"✓ Updated: {html_file.relative_to(root)}")
            updated += 1
    
    print(f"\n{'='*60}")
    print(f"Processed {len(html_files)} files, updated {updated}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
