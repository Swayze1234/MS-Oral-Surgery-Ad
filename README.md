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

## Contour Airlines package (`contour/`)

`contour/` holds the revised Contour Airlines proposal built after Clint Ostler's
Sept 30, 2026 reply (Oxford only, two flights, nothing billed Dec 6 to Jan 17):

- `onepager.html` / `onepager.pdf` — "The Round Trip" one-page offer ($3,600, two checks of $1,800).
- `order.html` / `order.pdf` — three-page insertion order MCTV-20261001-CNTR.
- `reply-email.md` — draft reply for Creed to review. Not sent to Contour.
- `agreement.html` / `agreement.pdf` — the contract, order MCTV-20261002-CNTR, in the MCTV one-page agreement format (plus Schedule A). Flight 1 only: $4,250 paid up front, 40 Oxford locations through Dec 5, flight board title through Jan 17, 2027, Kristin Garcia signing. Flight 2 is called out as not in the order.
- `fonts/` — Work Sans and Playfair Display (OFL) used by the agreement.
- `build.js` — renders the HTML files to PDF: `node contour/build.js`.
