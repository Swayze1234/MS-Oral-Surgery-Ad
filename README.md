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

# Client Proposal — Little & Holland PLLC (Oxford)

`MCTV_Proposal_Little_Holland_PLLC.pdf` is a 10-page proposal for **Stan Little,
Little & Holland PLLC**: two different 15-second commercials on **20, 40 or 80
screens** ($500 / $800 / $1,400 per month). It uses the same look as the media kit.

| Page | What's on it |
|------|--------------|
| 1 | Cover (Oxford stadium photo), prepared for Stan Little |
| 2 | Overview, why MCTV fits the firm, network stats |
| 3 | Partner logos *(media kit p2, reused)* |
| 4 | Storyboards for Spot A and Spot B (concepts) |
| 5 | How both spots run back-to-back every loop; what's included |
| 6 | Suggested Oxford venues + all 44 Oxford/Lafayette host venues |
| 7 | Local CPM comparison *(media kit p4, reused)* |
| 8 | 20 / 40 / 80-screen options, 6- and 12-month totals, prepay bonuses |
| 9 | Next steps + Swayze's contact info |
| 10 | Agreement & order form, pre-filled for Little & Holland |

## Rebuilding

```bash
pip install pymupdf jinja2 playwright
python3 build/little_holland/build_proposal.py
```

- Edit the words in `build/little_holland/copy.json`.
- Edit the layout in `build/little_holland/template.html`.
- Prices and the totals table come from `PLANS` in `build_proposal.py`.
- Photos and logos are pulled from `build/source/MCTV_Media_Kit_Oxford_original.pdf`
  at build time (into `build/little_holland/_assets/`, which isn't committed).
