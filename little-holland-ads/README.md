# Little & Holland PLLC — :15 spots for MCTV

| # | Spot | Audience | Status |
|---|------|----------|--------|
| 1 | `ad1-dui-students` — "DUI? Know Your Options." | College students | Draft v1 |
| 2 | Parents spot | Parents of college students | Not started |

## Spot 1 — storyboard (15 s, 1920×1080, 30 fps, silent)

| Time | Beat |
|------|------|
| 0.0–3.7 s | Blue police lights strobe in out of the dark → **DUI?** slams in with a camera shake → **KNOW YOUR OPTIONS.** wipes in |
| 3.9–8.3 s | Lights dim → *You're an adult.* / **What you tell us stays between us.** → lock clicks shut: PRIVATE & CONFIDENTIAL |
| 8.2–10.6 s | Lights back up → **CALL LITTLE & HOLLAND** / **662.232.9500** (digits drop in, phone badge rings) |
| 10.6–15.0 s | Light flash → logo outro: monogram ring draws, wordmark letters resolve, gold rule, *PLLC · Attorneys at Law · Oxford, Mississippi*, phone number, light sheen across the name |

The strobe keeps each light to 2 flashes per second, under the 3-per-second
photosensitivity guideline for public screens.

**Placeholder:** the outro logo (L&H monogram + serif wordmark) is a stand-in
until the firm's real logo file is supplied.

## Outputs (`out/`)

- `*_1080p_MASTER.mp4` — high-quality master (H.264 High, CRF 12, BT.709).
- `*_1080p_MCTV_700k.mp4` — MCTV network spec from the media kit
  (1920×1080 MP4, 300–700 kb/s, < 20 MB), two-pass encoded.

## Rebuilding

Each spot is an HTML page whose animation is driven by `window.seek(t)`, so
every frame is exact. Open `ad1-dui-students/index.html` in Chrome for a live
preview, or render:

```bash
cd little-holland-ads
npm i playwright            # once (or use a global install)
node render.cjs ad1-dui-students --name LittleHolland_DUI_Students_15s
node render.cjs ad1-dui-students --stills 2.6,6.4,9.3,14.9   # quick preview frames
```

Requires `ffmpeg`. Fonts (Anton, Montserrat, Cormorant Garamond — all SIL OFL)
are in `fonts/`.
