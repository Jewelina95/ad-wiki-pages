#!/bin/bash
# AD WIKI — local viewer launcher
# Starts a Python HTTP server in this directory and opens dashboard.html in your default browser.

set -e
cd "$(dirname "$0")"

PORT="${PORT:-8765}"
URL="http://localhost:${PORT}/dashboard.html"

# Refresh dashboard from latest wiki state
if command -v python3 >/dev/null 2>&1; then
  python3 code/scripts/build_dashboard.py >/dev/null 2>&1 || true
fi

echo ""
echo "  AD WIKI dashboard"
echo "  ──────────────────────────────────────────"
echo "  serving at: ${URL}"
echo "  press Ctrl+C to stop"
echo ""

# Open browser (macOS / Linux / WSL)
if command -v open >/dev/null 2>&1; then
  ( sleep 0.6 && open "${URL}" ) &
elif command -v xdg-open >/dev/null 2>&1; then
  ( sleep 0.6 && xdg-open "${URL}" ) &
fi

exec python3 -m http.server "${PORT}"
