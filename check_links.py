#!/usr/bin/env python3
import os
import re
from pathlib import Path
from collections import defaultdict

# Find all HTML files (excluding templates and email files)
html_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') and not file.startswith('email-'):
            filepath = os.path.join(root, file)
            html_files.append(filepath)

# Track all internal links
all_links = []
broken_links = []

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all href links
    href_pattern = r'href=["\']([^"\'#][^"\']*)["\']'
    matches = re.findall(href_pattern, content)
    
    for link in matches:
        # Skip external links
        if link.startswith('http://') or link.startswith('https://'):
            if 'novagenai.com.my' not in link:
                continue
            # Extract path from novagenai.com.my URLs
            if 'novagenai.com.my/' in link:
                link = '/' + link.split('novagenai.com.my/')[-1]
            else:
                continue
        
        # Skip anchors, mailto, tel, javascript
        if link.startswith('#') or link.startswith('mailto:') or link.startswith('tel:') or link.startswith('javascript:'):
            continue
        
        # Remove trailing anchor
        clean_link = link.split('#')[0]
        if not clean_link:
            continue
        
        # Resolve relative paths
        base_dir = os.path.dirname(html_file)
        if clean_link.startswith('/'):
            target_path = '.' + clean_link
        else:
            target_path = os.path.normpath(os.path.join(base_dir, clean_link))
        
        # Check if target exists
        exists = os.path.exists(target_path) or os.path.exists(target_path + '/index.html')
        
        if not exists:
            broken_links.append({
                'source': html_file,
                'link': link,
                'resolved': target_path
            })

print("=" * 80)
print("BROKEN INTERNAL LINKS")
print("=" * 80)
if broken_links:
    for item in broken_links[:20]:  # Show first 20
        print(f"\nSource: {item['source']}")
        print(f"  Link: {item['link']}")
        print(f"  Resolved to: {item['resolved']}")
else:
    print("✓ No broken internal links found!")

print("\n" + "=" * 80)
print(f"Total broken links: {len(broken_links)}")
print("=" * 80)
