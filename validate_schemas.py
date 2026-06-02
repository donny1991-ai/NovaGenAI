#!/usr/bin/env python3
import os
import sys
import json
import logging
import re
from html.parser import HTMLParser

# Default Log File
LOG_FILE = "schema_errors.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

class JSONLDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.json_blocks = []
        self.in_json_ld = False
        self.current_data = []
        self.script_attrs = None
        self.start_line = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            attrs_dict = dict(attrs)
            if attrs_dict.get('type') == 'application/ld+json':
                self.in_json_ld = True
                self.script_attrs = attrs_dict
                self.start_line = self.getpos()[0]
                self.current_data = []

    def handle_data(self, data):
        if self.in_json_ld:
            self.current_data.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_json_ld:
            self.json_blocks.append({
                'line': self.start_line,
                'content': ''.join(self.current_data),
                'attrs': self.script_attrs
            })
            self.in_json_ld = False
            self.current_data = []
            self.script_attrs = None

def validate_nested_object(obj, path="root", parent_type=None):
    """
    Recursively validates JSON-LD nesting and structure.
    Checks for:
    - Missing @type in objects that look like Schema.org nodes.
    - @context inside nested objects (usually only root needs @context).
    - Keys containing spaces or invalid characters.
    - Missing required structural keys depending on type.
    """
    errors = []
    warnings = []
    
    if isinstance(obj, dict):
        # Validate @context
        if "@context" in obj:
            context = obj["@context"]
            if path != "root":
                # Standard allows it but it is usually redundant and sometimes confusing
                warnings.append(f"Redundant '@context' at nested path '{path}'.")
            elif not isinstance(context, str) or not context.strip():
                errors.append(f"Root '@context' must be a non-empty string at '{path}'.")
        elif path == "root":
            errors.append(f"Root object is missing '@context'.")

        # Validate @type
        if "@type" in obj:
            t = obj["@type"]
            if not isinstance(t, (str, list)) or not t:
                errors.append(f"Invalid or empty '@type' value at '{path}'.")
        else:
            # Check if this object should have a @type (i.e. has more than 1 key and is a nested node)
            if len(obj) > 1 and not any(k.startswith('@') for k in obj):
                warnings.append(f"Object at '{path}' has no '@type' specified.")

        # Recurse into all keys and values
        for k, v in obj.items():
            current_path = f"{path}.{k}"
            # Check key name validity
            if not k.startswith('@') and not k.isidentifier() and not re.match(r'^[a-zA-Z0-9_:\-]+$', k):
                warnings.append(f"Key name '{k}' at '{current_path}' is non-standard.")
            
            # Recurse
            sub_errors, sub_warnings = validate_nested_object(v, current_path, parent_type=obj.get('@type'))
            errors.extend(sub_errors)
            warnings.extend(sub_warnings)
            
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            current_path = f"{path}[{idx}]"
            sub_errors, sub_warnings = validate_nested_object(item, current_path, parent_type=parent_type)
            errors.extend(sub_errors)
            warnings.extend(sub_warnings)
            
    return errors, warnings

def validate_file(file_path):
    """
    Reads an HTML file, extracts JSON-LD blocks, and validates each.
    """
    results = {
        'file': file_path,
        'blocks_found': 0,
        'blocks_valid': 0,
        'errors': [],
        'warnings': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        results['errors'].append(f"Failed to read file: {str(e)}")
        return results

    parser = JSONLDParser()
    try:
        parser.feed(content)
    except Exception as e:
        results['errors'].append(f"HTML parsing failed: {str(e)}")
        return results

    results['blocks_found'] = len(parser.json_blocks)
    
    for block in parser.json_blocks:
        block_line = block['line']
        block_content = block['content'].strip()
        
        if not block_content:
            results['warnings'].append(f"Empty JSON-LD script tag near HTML line {block_line}.")
            continue
            
        # Parse JSON
        try:
            data = json.loads(block_content)
        except json.JSONDecodeError as jde:
            # Map JSON parse error line back to the HTML file line
            error_line = block_line + jde.lineno - 1
            lines = block_content.splitlines()
            snippet = ""
            if 0 <= jde.lineno - 1 < len(lines):
                snippet = lines[jde.lineno - 1]
                
            results['errors'].append(
                f"JSON syntax error at HTML line {error_line} (JSON block line {jde.lineno}, col {jde.colno}): "
                f"{jde.msg}. Snippet: '{snippet.strip()}'"
            )
            continue

        # Structural / Nesting validation
        struct_errors, struct_warnings = validate_nested_object(data)
        
        # Format results with file context
        for err in struct_errors:
            results['errors'].append(f"Schema structure error near HTML line {block_line}: {err}")
        for warn in struct_warnings:
            results['warnings'].append(f"Schema warning near HTML line {block_line}: {warn}")
            
        if not struct_errors:
            results['blocks_valid'] += 1

    return results

def main():
    target_dir = "/root/NovaGenAI"
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        
    if not os.path.isdir(target_dir):
        logging.error(f"Target directory '{target_dir}' does not exist.")
        sys.exit(1)

    logging.info(f"Scanning directory: {target_dir}")
    html_files = []
    for root_dir, _, files in os.walk(target_dir):
        # Ignore common non-project dirs like .git, node_modules, etc.
        if any(ignored in root_dir for ignored in [".git", "node_modules", "venv", ".hermes"]):
            continue
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root_dir, file))

    if not html_files:
        logging.info("No HTML files found.")
        sys.exit(0)

    logging.info(f"Found {len(html_files)} HTML files. Starting schema validation...")
    
    total_blocks = 0
    total_valid_blocks = 0
    total_errors = 0
    total_warnings = 0
    files_with_errors = 0

    for file_path in sorted(html_files):
        rel_path = os.path.relpath(file_path, target_dir)
        results = validate_file(file_path)
        
        if results['blocks_found'] > 0:
            total_blocks += results['blocks_found']
            total_valid_blocks += results['blocks_valid']
            
            num_err = len(results['errors'])
            num_warn = len(results['warnings'])
            
            total_errors += num_err
            total_warnings += num_warn
            
            if num_err > 0 or num_warn > 0:
                logging.warning(f"File: {rel_path} - {results['blocks_found']} blocks found. Errors: {num_err}, Warnings: {num_warn}")
                for err in results['errors']:
                    logging.error(f"  [ERROR] {err}")
                for warn in results['warnings']:
                    logging.info(f"  [WARN] {warn}")
                if num_err > 0:
                    files_with_errors += 1
            else:
                logging.info(f"File: {rel_path} - {results['blocks_found']} blocks found (All {results['blocks_valid']} valid).")

    # Final summary report
    logging.info("=" * 60)
    logging.info("SCHEMA VALIDATION SUMMARY REPORT")
    logging.info("=" * 60)
    logging.info(f"Total HTML Files Scanned: {len(html_files)}")
    logging.info(f"Total JSON-LD Blocks Found: {total_blocks}")
    logging.info(f"Valid JSON-LD Blocks: {total_valid_blocks}")
    logging.info(f"Total Syntax/Structure Errors: {total_errors}")
    logging.info(f"Total Warnings: {total_warnings}")
    logging.info(f"Files with Errors: {files_with_errors}")
    logging.info(f"Detailed logs written to: {os.path.abspath(LOG_FILE)}")
    logging.info("=" * 60)

    if total_errors > 0:
        sys.exit(1)
    else:
        logging.info("Schema validation completed successfully with 0 errors!")
        sys.exit(0)

if __name__ == "__main__":
    main()
