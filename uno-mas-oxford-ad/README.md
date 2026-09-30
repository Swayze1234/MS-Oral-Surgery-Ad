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
| 0–5.0s | **Intro.** White tiles flip in over charcoal to build a tile wall. The sugar-skull logo pops on (skull, flowers, then the UNO MAS letters drop in and bounce). "TACOS & TEQUILA", "OXFORD, MISSISSIPPI", address · phone · website, lime ticker along the bottom. |
| 5.0–10.0s | **Street tacos, elevated.** Client's lime-squeeze photo in an arch window on the right, slow zoom. Rotating lime sticker badge. |
| 10.0–15.0s | **Tortas, fajitas & fries.** Charcoal background. Two stacked polaroids slide in: the client's torta-tray photo behind, and in front a polaroid that *plays* — three slowed video shots (chicken tacos → carne asada fries → sizzling fajitas) with crossfades. "MORE THAN TACOS" sticker. |
| 15.0–20.0s | **Full bar. Full table.** Full-bleed video: the bar shelf (Cathead vodkas) crossfading into the big overhead spread of plates. Kicker "Agaveria & taqueria" (their own mural wording). |
| 20.0–25.2s | **Find us in Oxford.** Postcard layout: the **white Oxford building** plays in a 1920x720 strip on top (drone aerial → side view → wide street front) while a white info band slides up with address, hours, phone. A small "Look for the white building" pill sits over the footage. |
| 25.2–30s | **Outro.** Logo, "TACOS & TEQUILA", @unomastacos, charcoal ticket card with address / hours / phone; lime stub flips open with unomastacos.com · Dine in · Takeout · Delivery. |

## Footage

The client's Vimeo video (`assets/source/uno_mas_vimeo_720p.mp4`, 1280x640,
23.98 fps) is a fast-cut piece where every shot is exactly 1 second long. The
shots used here are slowed ~2x with motion interpolation so each holds for about
2 seconds, then cropped to the size each scene needs and written out as 30 fps
JPEG frame sequences that the page swaps in per frame:

| Clip | Source time | Used in |
|------|-------------|---------|
| `p_tacos`, `p_fries`, `p_fajitas` | 43s, 30s, 4s | Scene 3 polaroid (924x617) |
| `f_bar`, `f_spread` | 18s, 45–48s | Scene 4 full bleed (1920x1080) |
| `b_aerial`, `b_side`, `b_wide` | 0s, 14s, 41s | Scene 5 building strip (1920x720) |

Shots at 17s, 36s and 8s were skipped because they show Christmas bows,
garland or a wreath. The frame folders under `assets/clips/*/` are generated
(~100 MB) and git-ignored; `assets/clips/manifest.js` (frame counts) is
committed. Rebuild them with:

```bash
pip install imageio-ffmpeg
python3 tools/make_clips.py            # all clips, a few minutes
python3 tools/make_clips.py b_wide     # just one
```

To swap a shot, change its entry in `SHOTS` inside `tools/make_clips.py`
(source start, duration, slow factor, size, crop offset), rebuild that clip, and
adjust the matching `SHOTS` list in `ad.html` if the timing changes.

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
