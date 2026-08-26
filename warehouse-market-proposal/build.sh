#!/bin/bash
# Renders proposal.html to ../Warehouse_Market_Host_Partnership_Proposal_August2026.pdf
set -e
cd "$(dirname "$0")"
CHROME="${CHROME:-/opt/pw-browsers/chromium}"
"$CHROME" --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="../Warehouse_Market_Host_Partnership_Proposal_August2026.pdf" \
  "file://$(pwd)/proposal.html"
echo "Wrote ../Warehouse_Market_Host_Partnership_Proposal_August2026.pdf"
