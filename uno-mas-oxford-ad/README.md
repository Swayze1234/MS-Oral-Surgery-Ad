# Uno Mas Tacos & Tequila — Oxford, MS — 30s silent digital ad (1920x1080)

`out/uno-mas-oxford-30s-1920x1080.mp4` is a 30-second, silent, 1920x1080 H.264
ad for the **Oxford** Uno Mas location only. It mixes the client's two stills
with slowed-down shots from their Vimeo video (the white Oxford building and
food only — no Starkville footage). It is deliberately styled differently from
the Starkville spot (`uno-mas-ad/` on branch `claude/beautiful-mayer-3v06fd`):

| | Starkville spot | Oxford spot (this one) |
|---|---|---|
| Palette | Red / cream / mustard | White / charcoal / lime, brand red as accent |
| Type | Bebas Neue (condensed) + Montserrat | Alfa Slab One (chunky slab) + Barlow + Fraunces italic |
| Intro | Sunburst + confetti | White subway-tile wall flips in, logo pops on |
| Photo framing | Split panes, full bleed | Arch window, stacked polaroids, postcard strip |
| Transitions | Skewed diagonal wipe | Vertical blinds |
| Outro | Dark, two locations | White, Oxford-only "ticket" with tear-off stub |

## Storyboard

| Time | Scene |
|------|-------|
| 0–5.0s | **Intro.** White tiles flip in over charcoal to build a tile wall (done by ~0.9 s). The sugar-skull logo pops on (skull, flowers, then the UNO MAS letters drop in and bounce), "TACOS & TEQUILA", "OXFORD, MISSISSIPPI" — settled by ~3.1 s and held. Lime ticker along the bottom. |
| 5.0–10.0s | **Street tacos, elevated.** Client's lime-squeeze photo in an arch window on the right (zoom anchored on the lime). Kicker "Open daily from 11 AM", sub "Classic Mexican fare, upgraded." Rotating lime sticker badge overlapping the arch corner. |
| 10.0–15.0s | **Tortas, fajitas & fries.** Charcoal background, white UNO MAS wordmark top-left. Two stacked polaroids slide in: the client's torta-tray photo behind, and in front a polaroid that *plays* three slowed shots in headline order (torta → sizzling fajitas → carne asada fries). "MORE THAN TACOS" sticker, kicker "Bring an appetite", sub "Burritos · Enchiladas · Desserts". |
| 15.0–20.0s | **Full bar. Full table.** Full-bleed video: the bar shelf (Cathead) for 1.7 s, then the big overhead spread; "Full table." lands as the spread resolves. Kicker "Tequila bar & taqueria", sub "Tequila · Margaritas · 1101 E Jackson Ave, Oxford". 300 px badge top-right. |
| 20.0–25.2s | **Find us in Oxford.** Postcard layout: the **white Oxford building** plays in a 1920x720 strip on top (wide street front → side view → drone aerial) while a white band slides up: kicker "Open daily from 11 AM", headline, then the address and phone at 44 px. An ink "Look for the white building" pill and a skull badge stamp straddle the seam. |
| 25.2–30s | **Outro.** Logo, "TACOS & TEQUILA", @unomastacos, charcoal ticket: "Come hungry.", address, hours, 56 px lime phone; lime stub flips open with unomastacos.com · Dine in · Takeout · Full bar. |

Scene cuts are vertical blinds; slat colour alternates (charcoal with lime edges, lime with charcoal edges into/out of the dark polaroid scene) and direction alternates per cut.

## Footage

The client's Vimeo video (`assets/source/uno_mas_vimeo_720p.mp4`, 1280x640,
23.98 fps) is a fast-cut piece where every shot is exactly 1 second long. The
shots used here are slowed ~2–2.6x with motion interpolation so each holds for
about 2 seconds, lightly graded (a touch more contrast/saturation on food, a
warm balance on the building), cropped to the size each scene needs and written
out as 30 fps JPEG frame sequences that the page swaps in per frame:

| Clip | Source time | Used in |
|------|-------------|---------|
| `p_torta`, `p_fajitas`, `p_fries` | 20s, 4s, 30s | Scene 3 polaroid (924x617) |
| `f_bar`, `f_spread` | 18s, 45.1–46.5s | Scene 4 full bleed (1920x1080) |
| `b_wide`, `b_side`, `b_aerial` | 41s, 14s, 0s | Scene 5 building strip (1920x720) |

Shots at 17s, 36s and 8s were skipped because they show Christmas bows,
garland or a wreath; `b_side` is zoomed 12.5% so the wreath at its right edge
is out of frame; `f_spread` stops at 46.5 s, before the video's baked-in fade
to black. The frame folders under `assets/clips/*/` are generated (~100 MB) and
git-ignored; `assets/clips/manifest.js` (frame counts) is committed. Rebuild
them with:

```bash
pip install imageio-ffmpeg
python3 tools/make_clips.py            # all clips, a few minutes
python3 tools/make_clips.py b_wide     # just one
```

To swap a shot, change its entry in `SHOTS` inside `tools/make_clips.py`
(source start, duration, slow factor, size, crop offset, grade), rebuild that
clip, and adjust the matching `SHOTS` list in `ad.html` if the timing changes.
Every clip must have frames through the end of its window plus the crossfade
(frame indices clamp to the last frame otherwise).

## Business info used

Pulled from public listings (site not reachable from the build environment):

- 1101 E Jackson Ave, Oxford, MS 38655 · (662) 371-9899
- unomastacos.com · @unomastacos
- Hours are shown only as "Open daily from 11 AM" — listings disagree on
  closing times (10/11 PM vs. 1 AM Thu–Sat), so confirm with the client before
  adding a closing time.
- Service claims are kept to "Dine in · Takeout · Full bar" (delivery removed
  until the client confirms it); "small-batch" / "handcrafted" adjectives were
  dropped because the footage does not support them.

Photos: `assets/lime-squeeze.jpg` and `assets/torta-tray.jpg` (client-supplied);
`assets/logo.png` + `assets/logo_glyphs.js` are shared with the Starkville spot
(vectorized so every logo piece animates independently and stays sharp).

## Editing / rebuilding

Everything is one HTML page driven by an async `render(t)` function, so the ad
is deterministic and can be previewed in any browser: open `ad.html#play`
(after generating the clips).

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
