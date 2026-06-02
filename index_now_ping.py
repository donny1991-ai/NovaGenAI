#!/usr/bin/env python3
"""
index_now_ping.py

Parses sitemap.xml from the project root, extracts all active URLs, and
pings the IndexNow API to trigger immediate indexing of the site pages.
Also performs a discrepancy check between physical HTML files in the repo
and URLs defined in the sitemap.xml.
Logs all activities to console and index_now_ping.log.
"""

import os
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import json
import datetime
import sys

# Configurations
DOMAIN = "novagenai.com.my"
BASE_URL = f"https://{DOMAIN}"
SITEMAP_FILE = "sitemap.xml"
INDEX_NOW_KEY = "93904c29a0ae4128a677c8e72d025d64"
KEY_LOCATION = f"{BASE_URL}/{INDEX_NOW_KEY}.txt"
LOG_FILE = "index_now_ping.log"

INDEX_NOW_ENDPOINTS = [
    "https://api.indexnow.org/IndexNow",
    "https://www.bing.com/IndexNow",
    "https://yandex.com/indexnow"
]

def log_message(message, log_file_obj=None):
    """Prints a message to console and writes to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    if log_file_obj:
        log_file_obj.write(formatted + "\n")
        log_file_obj.flush()

def parse_sitemap(sitemap_path, log_file):
    """Parses sitemap.xml and returns a list of URLs."""
    if not os.path.exists(sitemap_path):
        log_message(f"ERROR: Sitemap file not found at {sitemap_path}", log_file)
        return []
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # Namespace handling for sitemap
        namespace = ""
        if root.tag.startswith("{"):
            namespace = root.tag.split("}")[0] + "}"
        
        urls = []
        for url_node in root.findall(f"{namespace}url"):
            loc_node = url_node.find(f"{namespace}loc")
            if loc_node is not None and loc_node.text:
                urls.append(loc_node.text.strip())
                
        log_message(f"Successfully parsed {len(urls)} URLs from {sitemap_path}", log_file)
        return urls
    except Exception as e:
        log_message(f"ERROR: Failed to parse sitemap.xml: {e}", log_file)
        return []

def scan_html_files(root_dir):
    """Scans repository recursively for HTML files, excluding templates, backups, node_modules etc."""
    html_files = []
    exclude_dirs = {".git", "node_modules", "screenshots", "images", "infra", "assets"}
    exclude_files = {
        "email-template-lead.html",
        "email-preview.html",
        "404.html"
    }
    
    for root, dirs, files in os.walk(root_dir):
        # In-place modification to skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith("_") and not d.startswith(".")]
        
        for file in files:
            if not file.endswith(".html"):
                continue
            if file.startswith("_"):
                continue
            if file in exclude_files:
                continue
            
            # Compute relative path from root_dir
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)
            html_files.append(rel_path)
            
    return html_files

def map_file_to_url(rel_path):
    """Maps a physical HTML file relative path to its production URL."""
    # Normalize slashes
    rel_path = rel_path.replace("\\", "/")
    
    if rel_path == "index.html":
        return f"https://{DOMAIN}/"
    elif rel_path.endswith("/index.html"):
        # e.g., blog/index.html -> blog/
        return f"https://{DOMAIN}/{rel_path[:-10]}"
    else:
        return f"https://{DOMAIN}/{rel_path}"

def run_discrepancy_check(sitemap_urls, repo_dir, log_file):
    """Compares actual HTML files with URLs defined in sitemap.xml."""
    log_message("Starting sitemap discrepancy check against actual repo files...", log_file)
    
    # Get HTML files from repo
    repo_files = scan_html_files(repo_dir)
    
    # Map repo files to public URLs
    repo_urls = set(map_file_to_url(f) for f in repo_files)
    sitemap_set = set(sitemap_urls)
    
    log_message(f"Found {len(repo_files)} active HTML files in repository.", log_file)
    
    # Check 1: In repo but NOT in sitemap
    missing_in_sitemap = repo_urls - sitemap_set
    if missing_in_sitemap:
        log_message(f"WARNING: Found {len(missing_in_sitemap)} files in repository that are NOT listed in sitemap.xml:", log_file)
        for url in sorted(missing_in_sitemap):
            log_message(f"  - [Missing in Sitemap] {url}", log_file)
    else:
        log_message("OK: All active HTML files in repository are listed in sitemap.xml.", log_file)
        
    # Check 2: In sitemap but NOT in repo
    missing_in_repo = sitemap_set - repo_urls
    if missing_in_repo:
        log_message(f"WARNING: Found {len(missing_in_repo)} URLs in sitemap.xml that do NOT correspond to active physical HTML files:", log_file)
        for url in sorted(missing_in_repo):
            log_message(f"  - [Missing in Repo] {url}", log_file)
    else:
        log_message("OK: All sitemap URLs correspond to actual active HTML files in the repository.", log_file)
        
    return len(missing_in_sitemap) == 0 and len(missing_in_repo) == 0

def ping_index_now(urls, log_file):
    """Pings IndexNow API endpoints with the list of URLs."""
    if not urls:
        log_message("No URLs to submit to IndexNow.", log_file)
        return False
    
    payload = {
        "host": DOMAIN,
        "key": INDEX_NOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    
    json_data = json.dumps(payload).encode('utf-8')
    success_endpoints = 0
    
    log_message(f"Pinging {len(INDEX_NOW_ENDPOINTS)} IndexNow endpoints with {len(urls)} URLs...", log_file)
    
    for endpoint in INDEX_NOW_ENDPOINTS:
        log_message(f"Sending POST to {endpoint} ...", log_file)
        req = urllib.request.Request(
            endpoint,
            data=json_data,
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'IndexNow-Ping-Bot/1.0'
            },
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                status_code = response.getcode()
                response_text = response.read().decode('utf-8')
                log_message(f"SUCCESS: {endpoint} returned Status Code {status_code}. Response: '{response_text}'", log_file)
                success_endpoints += 1
        except urllib.error.HTTPError as e:
            status_code = e.code
            try:
                error_response = e.read().decode('utf-8')
            except Exception:
                error_response = "Unable to read error response body."
            log_message(f"HTTP ERROR: {endpoint} returned Status Code {status_code}. Response: '{error_response}'", log_file)
        except urllib.error.URLError as e:
            log_message(f"CONNECTION ERROR: Failed to reach {endpoint}. Reason: {e.reason}", log_file)
        except Exception as e:
            log_message(f"UNEXPECTED ERROR pinging {endpoint}: {e}", log_file)
            
    log_message(f"IndexNow Submission Finished. Successful endpoints: {success_endpoints}/{len(INDEX_NOW_ENDPOINTS)}", log_file)
    return success_endpoints > 0

def main():
    # Make sure we're in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f_log:
        log_message("="*60, f_log)
        log_message("IndexNow Automated Pinger Execution Started", f_log)
        log_message("="*60, f_log)
        
        # 1. Parse Sitemap
        sitemap_path = os.path.join(script_dir, SITEMAP_FILE)
        sitemap_urls = parse_sitemap(sitemap_path, f_log)
        
        if not sitemap_urls:
            log_message("CRITICAL: No URLs found. Exiting.", f_log)
            sys.exit(1)
            
        # 2. Perform Discrepancy Check
        run_discrepancy_check(sitemap_urls, script_dir, f_log)
        
        # 3. Ping IndexNow APIs
        success = ping_index_now(sitemap_urls, f_log)
        
        log_message("="*60, f_log)
        if success:
            log_message("IndexNow Automated Pinger completed successfully.", f_log)
        else:
            log_message("IndexNow Automated Pinger completed with errors/failures.", f_log)
        log_message("="*60, f_log)

if __name__ == "__main__":
    main()
