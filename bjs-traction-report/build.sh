#!/bin/bash
# Renders report.html to ../BJs_Family_Pharmacy_Traction_Report_August2026.pdf
# Requires Chromium (any recent build). Adjust CHROME if needed.
set -e
cd "$(dirname "$0")"
CHROME="${CHROME:-/opt/pw-browsers/chromium}"
"$CHROME" --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer --print-to-pdf-no-header \
  --print-to-pdf="../BJs_Family_Pharmacy_Traction_Report_August2026.pdf" \
  "file://$(pwd)/report.html"
echo "Wrote ../BJs_Family_Pharmacy_Traction_Report_August2026.pdf"
