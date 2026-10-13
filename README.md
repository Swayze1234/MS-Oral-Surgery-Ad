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

# Client Proposal — Stan Little (Little & Holland + rental car business)

`MCTV_Proposal_Little_Holland_PLLC.pdf` is a 2-page, portrait (Letter) proposal
for **Stan Little**. Stan already has the Oxford media kit, so this sticks to
options and pricing.

**Page 1: options & pricing**
1. **Little & Holland, PLLC: 15-second commercial.** Pick one option:
   20 screens $500/mo · 40 screens $800/mo · 80 screens $1,400/mo ·
   80 screens + Oxford traffic-updates sponsorship $2,000/mo (Stan picks which business sponsors it).
2. **Rental car business: 30-second commercial, 50% off** the matching screen
   rate, on the same screens ($250 / $400 / $700 per month).
3. **Pay up front & save:** 6 months up front → 7th month free; 12 months up
   front → 13th & 14th months free. The table shows totals for Little & Holland
   only and for both businesses.

**Page 2: agreement & order form**, pre-filled for Stan / Little & Holland.

## Rebuilding

```bash
pip install pymupdf jinja2 playwright pillow numpy
python3 build/little_holland/build_proposal.py
```

- Prices, ad plays and the 50% rental discount: top of `build/little_holland/build_proposal.py`
  (`SCREEN_RATE`, `PLAYS`, `RENTAL_DISCOUNT`, `OPTIONS`). All totals are calculated from these.
- Wording: `build/little_holland/copy.json`. Layout: `build/little_holland/template.html`.
- `little_holland_logo.png` is the firm's logo; its navy background is removed at build time.
- MCTV logos and Swayze's headshot are pulled from `build/source/MCTV_Media_Kit_Oxford_original.pdf`
  into `build/little_holland/_assets/` (not committed).
