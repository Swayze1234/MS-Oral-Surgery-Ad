# Parlor 1858 × MCTV — Host Partnership Proposal

`Parlor1858_MCTV_Host_Partnership.pdf` is a two-page, print-ready (US Letter) host
partnership proposal for Parlor 1858 (Oxford, MS), branded with the Parlor 1858 and
MCTV Elite Advertising logos and MCTV's navy/gold media-kit palette.

**Options presented**

| Option | What Parlor 1858 gives | What Parlor 1858 gets | Price |
|---|---|---|---|
| 1 · Host Exchange | 1 hosted MCTV screen in the parlor | Custom 30-second ad, free on MCTV screens in Oxford | $0 / mo |
| 2 · Host + Growth | 1 hosted screen + $500/mo | Everything in Option 1 + Google Business Profile management + 15 additional Oxford screens | $500 / mo |

## Files
- `partnership.html` — source document (edit copy/prices here).
- `parlor1858_logo.svg` — vector recreation of the Parlor 1858 logo.
- `mctv_logo.png` — MCTV logo, extracted from the media kit.
- `fonts/embedded.css` — Playfair Display + Inter embedded as base64 so the PDF renders identically anywhere.
- `render.py` — inlines the logo and fonts, then renders the PDF and page previews with Chromium.
- `preview_p1.png`, `preview_p2.png` — page previews.

## Rebuilding
```bash
pip install playwright
python3 render.py
```
