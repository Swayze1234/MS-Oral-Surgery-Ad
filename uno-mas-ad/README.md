# Uno Mas Tacos & Tequila — 30s silent digital ad (1920x1080)

`out/uno-mas-30s-1920x1080.mp4` is a 30-second, silent, 1920x1080 H.264 ad
for Uno Mas Tacos & Tequila (Starkville & Oxford, MS).

## Storyboard

| Time | Scene |
|------|-------|
| 0–6.5s | **Intro.** Red-to-cream pop reveal. The sugar-skull logo draws on as an outline, fills in, the side flowers bloom out, and the "UNO MAS" letters bounce in one at a time, followed by a confetti burst. "TACOS & TEQUILA" tracks in, and the contact bar (address · phone · website) slides up from the bottom of the frame. |
| 6.5–12.5s | **Tacos & Tequila.** Flat-lay photo (chips, queso, loaded fries) with slow zoom, headline "Tacos & Tequila", "A modern taqueria & agave bar", "Salsas, tortillas & chips made in-house daily". |
| 12.5–18.5s | **Fresh. Handcrafted. Fun.** Full-bleed al pastor close-up, headline reveals word by word. |
| 18.5–24.5s | **Agave bar.** "50+ Tequilas & Mezcals", "Handcrafted margaritas · Patio seating", "Open late Thu–Sat 'til 1 AM", game-day taco photo. |
| 24.5–30s | **Outro.** Logo, both locations with addresses and phone numbers, and a bottom bar with @unomastacos · unomastacos.com · Dine in · Takeout · Catering. |

Scene changes use a skewed red/mustard wipe. The logo pieces are vectorized
from `assets/logo.png` so every element (skull, flowers, sprigs, each letter)
animates independently and stays sharp at 1080p.

## Business info used

Pulled from public listings (the site itself was not reachable from the build
environment, so the site's own video is not included):

- Starkville · Cotton District — 106 Maxwell St, Starkville, MS 39759 · (662) 338-4644
- Oxford · The Square — 1101 E Jackson Ave, Oxford, MS 38655 · (662) 371-9899
- unomastacos.com · @unomastacos
- Starkville hours: Sun–Wed 11 AM–10 PM, Thu–Sat 11 AM–1 AM

## Editing / rebuilding

Everything is one HTML page driven by a `render(t)` function, so the whole ad
is deterministic and can be previewed in any browser: open `ad.html#play`.

- Copy, colors, timings: edit `ad.html` (timeline constants are in the `T`
  object; each scene has its own `renderS*` function).
- Photos: swap the files in `assets/` (same file names) or change the
  `object-position` on each `<img>` to re-crop.
- Logo: `assets/logo_glyphs.js` was generated from `assets/logo.png` with
  potrace (see `tools/vectorize_logo.py`).

Render the MP4 (needs Node with Playwright + Chromium, and an ffmpeg with
libx264; `pip install imageio-ffmpeg` provides one):

```bash
NODE_PATH=/opt/node22/lib/node_modules node render.cjs                 # full 30s MP4
NODE_PATH=/opt/node22/lib/node_modules node render.cjs --preview 2,9,15  # stills at given seconds
```

Frames are screenshotted at 1920x1080 / 30 fps in headless Chromium and piped
straight into ffmpeg (libx264, CRF 17, yuv420p, faststart).
