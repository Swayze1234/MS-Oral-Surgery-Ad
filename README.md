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

`MCTV_Proposal_Little_Holland_PLLC.pdf` is an 8-page landscape proposal for
**Stan Little**, styled after MCTV's Schwartz 2027 proposal (Playfair Display +
Barlow, navy/cream/gold, real-screen mockups). Stan already has the Oxford media
kit, so it sticks to the deal: options, prices, ad plays, pay-up-front savings,
terms and a sign-off page.

| Page | What's on it |
|------|--------------|
| 1 | Cover, with a Little & Holland mockup on a real MCTV screen |
| 2 | The proposal, in six lines |
| 3 | Four ways to build it: Little & Holland's :15 at 20 / 40 / 80 screens ($500 / $800 / $1,400) or 80 screens + MCTV Traffic sponsorship in Oxford ($2,000) |
| 4 | The rental car :30 at half the screen rate ($250 / $400 / $700), with totals for both businesses |
| 5 | Pay up front: 6 months → 7th free; 12 months → 13th & 14th free (totals for L&H only and both) |
| 6 | The terms, in plain words + MCTV Traffic + the Bar-filing notes for the law firm spot |
| 7 | Five steps and four questions, with Swayze's contact card |
| 8 | Pick your build and sign |

## Rebuilding

```bash
pip install pymupdf jinja2 playwright pillow numpy
python3 build/little_holland/build_proposal.py
```

- Prices, ad plays and the 50% rental discount: top of `build/little_holland/build_proposal.py`
  (`SCREEN_RATE`, `PLAYS`, `RENTAL_DISCOUNT`, `OPTIONS`). Every total is calculated from these.
- Layout and wording: `build/little_holland/template.html`; date and footer: `copy.json`.
- Fonts: `build/little_holland/fonts/` (Playfair Display and Barlow, SIL Open Font License).
- Photos: `build/little_holland/photos/`. These were made once by `make_mockups.py`, which
  takes room and Oxford photos from the Schwartz proposal PDF (not kept here) and
  puts the mock ads from `mockup_ads.html` onto the real screens. Re-run it only to
  change the mockups:
  `python3 build/little_holland/make_mockups.py /path/to/Schwartz-MCTV-2027-Exclusivity.pdf`
- `little_holland_logo.png` is the firm's logo; its navy background is removed at build time.
