# Uno Mas Tacos & Tequila — Oxford, MS — 30s silent digital ad (1920x1080)

`out/uno-mas-oxford-30s-1920x1080.mp4` is a 30-second, silent, 1920x1080 H.264
ad for the **Oxford** Uno Mas location only. It is deliberately styled
differently from the Starkville spot (`uno-mas-ad/` on branch
`claude/beautiful-mayer-3v06fd`):

| | Starkville spot | Oxford spot (this one) |
|---|---|---|
| Palette | Red / cream / mustard | White / charcoal / lime, brand red as accent |
| Type | Bebas Neue (condensed) + Montserrat | Alfa Slab One (chunky slab) + Barlow + Fraunces italic |
| Intro | Sunburst + confetti | White subway-tile wall flips in, logo pops on |
| Photo framing | Split panes, full bleed | Arch window, tilted polaroid card |
| Transitions | Skewed diagonal wipe | Vertical blinds |
| Outro | Dark, two locations | White, Oxford-only "ticket" with tear-off stub |

## Storyboard

| Time | Scene |
|------|-------|
| 0–6.2s | **Intro.** White tiles flip in over charcoal to build a tile wall. The sugar-skull logo pops on (skull, flowers, then the UNO MAS letters drop in and bounce). "TACOS & TEQUILA", "OXFORD, MISSISSIPPI", address · phone · website, and a lime ticker along the bottom. |
| 6.2–12.4s | **Street tacos, elevated.** Lime-squeeze photo in an arch window on the right, slow zoom. Headline "STREET TACOS, *elevated.*", rotating lime sticker badge. |
| 12.4–18.6s | **Tortas, fries & tequila.** Charcoal background, the torta-and-fries tray as a tilted polaroid card sliding in, "MORE THAN TACOS" sticker. |
| 18.6–24.6s | **Find us in Oxford.** Reserved for the **white Oxford building photo** (see below). Until the photo is added, a lime typographic panel with "1101 E JACKSON AVE" fills the right side. Address, hours, phone with icons. |
| 24.6–30s | **Outro.** Logo, "TACOS & TEQUILA", @unomastacos, and a charcoal ticket card with the address, hours and phone; the lime stub flips open with unomastacos.com · Dine in · Takeout · Delivery. |

## Adding the white building photo

The build environment could not reach `unomastacos.com` (blocked by the
session's network policy), so the Oxford storefront photo is not in the repo
yet. To drop it in:

1. Save the photo as `assets/building.jpg` (landscape, ideally 1920x1080 or
   larger; the building should sit in the right ~45% of the frame since the
   left side carries a white text scrim).
2. Optionally adjust `object-position` on `#s4-photo` in `ad.html` to re-crop.
3. Re-render (below). The page detects the file automatically: with it, scene 4
   is the full-bleed photo with a white gradient scrim; without it, the lime
   "1101" panel is used instead.

## Business info used

Pulled from public listings (site not reachable from the build environment):

- 1101 E Jackson Ave, Oxford, MS 38655 · (662) 371-9899
- unomastacos.com · @unomastacos
- Hours are shown only as "Open daily from 11 AM" — listings disagree on
  closing times (10/11 PM vs. 1 AM Thu–Sat), so confirm with the client before
  adding a closing time.

Photos: `assets/lime-squeeze.jpg` and `assets/torta-tray.jpg` (client-supplied);
`assets/logo.png` + `assets/logo_glyphs.js` are shared with the Starkville spot
(vectorized so every logo piece animates independently and stays sharp).

## Editing / rebuilding

Everything is one HTML page driven by a `render(t)` function, so the ad is
deterministic and can be previewed in any browser: open `ad.html#play`.

- Copy, colors, timings: edit `ad.html` (timeline in the `T` object; each scene
  has its own `renderS*` function; colors are CSS variables in `:root`).
- Fonts are self-hosted in `assets/fonts/` (Google Fonts: Alfa Slab One, Barlow,
  Barlow Condensed, Fraunces).

Render the MP4 (needs Node with Playwright + Chromium, and an ffmpeg with
libx264; `pip install imageio-ffmpeg` provides one):

```bash
NODE_PATH=/opt/node22/lib/node_modules node render.cjs                    # full 30s MP4
NODE_PATH=/opt/node22/lib/node_modules node render.cjs --preview 3,9,15   # stills at given seconds
```

Frames are screenshotted at 1920x1080 / 30 fps in headless Chromium and piped
into ffmpeg (libx264, CRF 17, yuv420p, faststart).
