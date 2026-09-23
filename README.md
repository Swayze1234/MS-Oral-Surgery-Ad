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

# Premier Aesthetics :30 TV Spot — 2026 Refresh

`premier-aesthetics-ad/MCTV_PremierAesthetics_FS_2026.mp4` replaces
`MCTV_48HPremierAesthetics_FS_In_1.mp4` (1920x1080, 29.97 fps, 30.03s, silent
stereo AAC track — same spec as the original).

| Time | Scene |
|------|-------|
| 0–2.6s | Original PA logo intro, dissolving into… |
| 2.6–10s | **New team group photo** (old photo removed), full-bleed with slow push-in, "Meet Our Team / Welcome to Premier Aesthetics" |
| 10–20s | Microneedling footage + "Summer Skin Prep — Essentials that aren't SPF" |
| 20–27s | Injectables footage + "Introducing Premier Perks" |
| 27–30s | **New end card**: logo, "Your natural beauty, elevated.", "Book your consultation today", phone, socials |

Refreshed look: Playfair Display + Montserrat type, gold accents, animated
text reveals, gentle zooms, and cross-dissolves between scenes.

Rebuild: `cd premier-aesthetics-ad && pip install pillow numpy imageio-ffmpeg && python3 build_ad.py`
