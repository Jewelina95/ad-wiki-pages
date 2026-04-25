#!/bin/bash
# AD WIKI Public — one-command update.
# Rebuilds dashboard.html from current wiki content, commits, and pushes.
# GitHub Pages auto-republishes within ~1 minute.

set -e
cd "$(dirname "$0")"

echo "→ Rebuilding dashboard..."
python3 code/scripts/build_dashboard.py

if [ -z "$(git status --porcelain)" ]; then
  echo "  No changes — nothing to publish."
  exit 0
fi

echo ""
echo "→ Changes detected:"
git status --short
echo ""

MSG="${1:-Update wiki content + dashboard rebuild}"
git add -A
git commit -m "$MSG"
git push

echo ""
echo "✅ Published."
echo "   Live URL: https://jewelina95.github.io/ad-wiki-pages/"
echo "   (Pages typically updates within 30-60 seconds)"
