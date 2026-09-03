# Warner Family Dentistry — Screen Traction Report

Client-facing report covering 4/6/2026 – 9/3/2026 on the Starkville MCTV network.

- `Warner_Family_Dentistry_Traction_Report.pdf` — send this to the client.
- `Warner_Family_Dentistry_Traction_Report.html` — same report as a web page (hover the chart for details).
- `source/` — the four MCTV player exports (one per spot version, FS_1–FS_4).

## Rebuilding

```bash
cd reports/warner-family-dentistry
pip install openpyxl
python3 agg.py            # combines the four xlsx exports into agg.json
python3 build_report.py   # writes the HTML report
/opt/pw-browsers/chromium --headless=new --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=Warner_Family_Dentistry_Traction_Report.pdf \
  "file://$PWD/Warner_Family_Dentistry_Traction_Report.html"
```

Edit the `SELECTED` list in `build_report.py` to change which screens count as paid vs. gifted.

## Logos

The header logos are vector recreations. To use the real artwork, save the
files as `logos/warner.png` and `logos/mctv.png` (transparent PNG, roughly
600px wide) and rerun `build_report.py`; the script embeds them automatically.
