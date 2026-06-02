#!/usr/bin/env python3
"""Run build_v5 by loading PAGES from build_v4."""
import sys, os
os.chdir("/root/NovaGenAI")

# Read build_v4.py and extract the PAGES list
with open("build_v4.py") as f:
    content = f.read()

# Find the PAGES = [...] block
start = content.find("PAGES = [")
end = content.rfind("for p in PAGES:")
pages_block = content[start:end].strip()

# Execute it to define PAGES
exec(pages_block)

# Now PAGES is defined. Load build_v5 and run its build function.
# Strip the exec line from build_v5 and run the rest
with open("build_v5.py") as f:
    v5 = f.read()

# Remove the problematic exec line
v5_clean = v5.replace(
    "exec(open(\"/root/NovaGenAI/build_v4.py\").read().split(\"# ── PAGE DATA ──\")[1].split(\"for p in PAGES:\")[0])",
    "# PAGES loaded from build_v4.py"
)

exec(v5_clean)
