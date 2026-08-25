# Financial Concepts — Advertiser Partnership Proposal

Builds `../Financial_Concepts_Proposal.pdf`: a 10-page, 11"×8.5" landscape booklet
(spiral-bound along the **top** edge — the top 0.55" of every page is kept clear of
content for the coil punch) for the Thursday Aug 27, 2026 meeting with Financial
Concepts' marketing team (Columbus, MS — fincon.net).

## Rebuilding

```bash
cd proposal
pip install pymupdf pillow
python3 build.py          # writes ../Financial_Concepts_Proposal.pdf
```

Pages print via headless Chromium (`/opt/pw-browsers/chromium` in Claude's remote
environment; point `CHROMIUM` in `build.py` at any Chrome/Chromium locally) and are
merged with PyMuPDF.

## Dropping in photos

Three folders are auto-detected by `build.py` — add images (jpg/png/webp) and rerun:

| Folder | Goes to | Slots |
|---|---|---|
| `assets/cover/` | Page 1 full-bleed cover background (Starkville mural photo) | first image, sorted by name |
| `assets/screens/` | Page 6 "Real screens, real venues" grid | 6, sorted by name |
| `assets/billboards/` | Page 7 screen mockups (their billboard creative) | 2, sorted by name |

Missing images leave a styled dashed placeholder, so the deck builds either way.
Venue captions on page 6 ("VENUE · MARKET") are edited directly in
`pages/p06_screens.html`.

## Files

- `pages/p01…p10*.html` — one file per booklet page, in order.
- `style.css` — brand tokens sampled from the MCTV North MS media kit (cream
  `#F6F4F0`, navy `#0B2044`, steel `#5E7391`; Playfair Display display serif,
  Barlow text) + shared page scaffolding.
- `fonts.css` + `assets/fonts/` — self-hosted Playfair Display & Barlow (latin).
- `extract_assets.py` — pulls the white MCTV wordmark out of the media kit PDF
  (pass the kit's path as an argument); `assets/mctv_logo_navy.png` is a recolor.
- `build.py` — injects photos, prints each page to PDF, merges, sets metadata.
