#!/bin/bash
set -e
cd "$(dirname "$0")/.."

# Generate single article placeholder
uv run python3 scripts/generate_one.py > /tmp/article_spec.json

# Read the spec
keyword=$(python3 -c "import json; print(json.load(open('/tmp/article_spec.json'))['keyword'])")
slug=$(python3 -c "import json; print(json.load(open('/tmp/article_spec.json'))['slug'])")

echo "=== Auto Site Build ==="
echo "Keyword: $keyword"
echo "Slug: $slug"
echo "Date: $(date +%Y-%m-%d)"

# Build site
uv run python3 scripts/site_builder.py

echo "=== Done ==="
echo "Site built at output/"
echo "To publish: cd output && git init && git add . && git commit -m 'update'"