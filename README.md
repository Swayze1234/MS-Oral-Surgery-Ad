# MCTV Media Kit — Tupelo Edition

`MCTV_Media_Kit_Tupelo.pdf` is a Tupelo-customized version of the MCTV Digital
advertiser media kit (originally built with Oxford imagery and Creed Cannon as
the contact).

## What changed vs. the original

| # | Page | Change |
|---|------|--------|
| 1 | Cover (p1) | Oxford / Ole Miss stadium photo → **Tupelo City Hall**, with a subtle navy scrim on the top-left so the white "Be impossible to ignore." headline stays legible over the brighter daytime shot. |
| 2 | Back (p11) | Oxford water-tower photo → **downtown Tupelo street scene**. |
| 3 | Contact block (p11) | "Creed Cannon · MCTV Digital" → **Swayze Hollingsworth · MCTV Digital**, `swayze@mctvofms.com · 662-907-0404`. |
| 4 | Footer (p11) | Mary Michael Cannon removed (text + headshot). **Swayze Hollingsworth is now the sole contact**, centered. |
| 5 | Signature (p12) | "CREED CANNON · MCTV DIGITAL / DATE" → **SWAYZE HOLLINGSWORTH · MCTV DIGITAL / DATE**. |

Everything else — partner logos, the host-location list (which spans Oxford,
Tupelo & the Golden Triangle), pricing, packages, and all copy — is unchanged,
since the network itself serves all three markets.

## Rebuilding

The kit is regenerated from the original PDF plus two Tupelo photos:

```bash
cd build
pip install pymupdf pillow numpy
python3 make_cover.py   # crops photos to 3:2 and bakes the cover scrim
python3 build.py        # applies image + text edits, writes ../MCTV_Media_Kit_Tupelo.pdf
```

### `build/` contents
- `make_cover.py` — prepares `cover.jpg` (with scrim) and `back.jpg` from the source photos.
- `build.py` — swaps the two photos and applies the contact/signature edits.
- `source/tupelo_city_hall_cover.jpg` — cover photo.
- `source/tupelo_downtown_backpage.jpg` — back-page photo.
- `source/MCTV_Media_Kit_Oxford_original.pdf` — the original (unmodified) kit.

To spin up another market version, drop in new photos and adjust the contact
strings in `build.py`.

---

# HOTWORX Oxford — Advertising Proposal

`MCTV_Proposal_HOTWORX_Oxford.pdf` is a 7-page, 16:9 advertising proposal for
HOTWORX (24 Hour Infrared Fitness Studio) in Oxford, MS, co-branded with the
HOTWORX and MCTV logos and using **regular** monthly network rates (no seasonal
specials, no add-ons).

| Page | Content |
|------|---------|
| 1 | Cover — MCTV + HOTWORX logos, Oxford stadium photo, Swayze Hollingsworth contact |
| 2 | The opportunity — why HOTWORX × MCTV, key stats, how it works |
| 3 | Network stats + local CPM comparison |
| 4 | All 44 Oxford / Lafayette host locations, grouped by venue type |
| 5 | Packages & pricing — 20 / 40 / 80 / 125+ screens, prepay bonus, inclusions |
| 6 | Next steps, contact, ad specs |
| 7 | Agreement & order form pre-filled for HOTWORX Oxford |

## Portrait version

`MCTV_Proposal_HOTWORX_Oxford_Letter.pdf` is a 3-page US Letter (portrait) version
in the Parlor 1858 proposal style (Playfair Display + Inter, navy/gold, white paper):

| Page | Content |
|------|---------|
| 1 | Logos, pitch, key stats, the four regular packages (40 screens recommended), prepay bonus, inclusions |
| 2 | All 44 Oxford host venues by type, CPM comparison, four steps to launch |
| 3 | Side-by-side package table, agreement & order form with signature lines |

## Rebuilding

```bash
pip install pymupdf playwright          # Chromium is pre-installed at /opt/pw-browsers
python3 build/hotworx/build_proposal.py # landscape: MCTV_Proposal_HOTWORX_Oxford.pdf
python3 build/hotworx/build_portrait.py # portrait:  MCTV_Proposal_HOTWORX_Oxford_Letter.pdf
```

Shared data (pricing, host list, logos, contact) lives in `build/hotworx/common.py`;
`build/hotworx/fonts/embedded.css` carries the Playfair Display + Inter fonts.

`build/hotworx/build_proposal.py` pulls the MCTV logos, photos, pricing and
host list from `build/source/MCTV_Media_Kit_Oxford_original.pdf`, generates
HTML, and prints it to PDF with headless Chromium. The HOTWORX wordmark is
drawn as inline SVG (`HOTWORX_SVG` in the script); swap in the official logo
file there if you have one.
