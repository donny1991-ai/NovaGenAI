#!/usr/bin/env python3
import os
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import urljoin, urlparse

# Find all HTML files
html_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') and not file.startswith('email-'):
            html_files.append(os.path.join(root, file))

# Parse internal links from each file
links_from = defaultdict(list)  # page -> [links it contains]
links_to = defaultdict(list)    # page -> [pages linking to it]

def normalize_path(path, base_file):
    """Normalize a link path relative to base file"""
    if path.startswith('http://') or path.startswith('https://'):
        if 'novagenai.com.my' in path:
            parsed = urlparse(path)
            return parsed.path if parsed.path else '/'
        return None  # External link
    
    # Remove anchors
    path = path.split('#')[0]
    if not path:
        return None
    
    # Handle absolute paths
    if path.startswith('/'):
        return path
    
    # Handle relative paths
    base_dir = os.path.dirname(base_file)
    full_path = os.path.normpath(os.path.join(base_dir, path))
    return full_path

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all href links
    href_pattern = r'href=["\']([^"\']+)["\']'
    matches = re.findall(href_pattern, content)
    
    for link in matches:
        normalized = normalize_path(link, html_file)
        if normalized:
            links_from[html_file].append(normalized)
            links_to[normalized].append(html_file)

# Generate report
print("=" * 80)
print("INTERNAL LINK STRUCTURE ANALYSIS")
print("=" * 80)
print()

print("1. LINK COUNT BY PAGE")
print("-" * 80)
for page in sorted(html_files):
    internal_count = len(links_from[page])
    print(f"{page:50} → {internal_count:3} internal links")
print()

print("2. ORPHAN PAGES (no incoming internal links)")
print("-" * 80)
orphans = []
for page in html_files:
    # Normalize page path for comparison
    norm_page = page.lstrip('./')
    if norm_page.startswith('/'):
        norm_page = norm_page[1:]
    
    # Check if page has incoming links
    has_incoming = False
    for target, sources in links_to.items():
        if norm_page in target or target.endswith(norm_page):
            has_incoming = True
            break
    
    if not has_incoming and page != './index.html':
        orphans.append(page)
        print(f"  • {page}")

if not orphans:
    print("  ✓ No orphan pages found")
print()

print("3. PAGES WITH FEWEST INTERNAL LINKS")
print("-" * 80)
sorted_by_links = sorted(html_files, key=lambda x: len(links_from[x]))
for page in sorted_by_links[:10]:
    count = len(links_from[page])
    print(f"  {count:3} links: {page}")
print()

print("4. TOP LINKED-TO PAGES")
print("-" * 80)
link_targets = defaultdict(int)
for sources in links_to.values():
    for source in sources:
        link_targets[source] += 1

for page, count in sorted(link_targets.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {count:3} incoming: {page}")
print()

print("=" * 80)
print(f"Total pages analyzed: {len(html_files)}")
print(f"Total unique link targets: {len(links_to)}")
print("=" * 80)
