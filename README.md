# MCTV Sales Collateral

## Starkville School District Proposal

`Starkville_School_District_Proposal.pdf` — 3-page print-ready proposal for
RoyAnn Bell / Starkville School District (Aug 2026): a $200 September welcome
offer on 10 screens (reg. $350/mo), the CPM case vs. outdoor billboards
($2.63 vs $6), and an October tiered menu (10/$350 · **20/$500 recommended** ·
40/$800) with a 12-month prepay pitch (months 13–14 free).

Source: `proposal/starkville_school_proposal.html`. Co-branded in Starkville
Oktibbeha School District colors — black `#141414` / gold `#F5B914` / cream
`#f9f6ef` — with a vector recreation of the district's confetti lockup
(`proposal/ssd_lockup.svg`; swap in the official logo file if provided).
Typefaces: Playfair Display + Work Sans. Rebuild with:

```bash
chromium --headless --no-pdf-header-footer \
  --print-to-pdf=Starkville_School_District_Proposal.pdf \
  proposal/starkville_school_proposal.html
```

(Work Sans and Playfair Display must be installed locally for a faithful render.)

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
