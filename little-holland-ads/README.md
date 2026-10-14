# Little & Holland PLLC — :15 spots for MCTV

| # | Spot | Audience | Status |
|---|------|----------|--------|
| 1 | `ad1-dui-students` — "DUI? Know Your Options." | College students | Draft v3 |
| 2 | Parents spot | Parents of college students | Not started |

## Spot 1 — storyboard (15 s, 1920×1080, 30 fps, silent)

| Time | Beat |
|------|------|
| 0.0–3.7 s | Blue police lights strobe in out of the dark → **DUI?** (ivory serif, gold “?”) slams in with a camera shake → gold fleur-de-lis divider draws out → **KNOW YOUR OPTIONS.** wipes in |
| 3.75–8.3 s | Split screen: the attorneys' photo wipes in on the left behind a glowing gold edge; on the right, *You're an adult.* (gold italic) / **What you tell us** (ivory) / **stays between us.** (gold) → gold lock clicks shut: PRIVATE & CONFIDENTIAL |
| 8.2–10.6 s | Lights back up → gold ring draws around Stan Little's portrait (*STAN LITTLE, ATTORNEY*) → **CALL LITTLE & HOLLAND** / **662.232.9500** (digits drop in) |
| 10.6–15.0 s | Light flash → logo outro: gold fleur-de-lis grows up, *LITTLE & HOLLAND, PLLC* resolves letter by letter, *CONCIERGE ATTORNEYS*, phone number, *Oxford, Mississippi*, Bar notice line, light sheen across the name |

All on-screen type follows the firm's branding to match the outro: Cormorant
Garamond (the logo's serif) in ivory and gold on navy, with Montserrat for the
phone number and small caps lines. The blue police lights stay in the background.

The strobe keeps each light to 2 flashes per second, under the 3-per-second
photosensitivity guideline for public screens.

**Logo:** the firm's logo file (`assets/little_holland_logo_reference.png`, from
the proposal) is only 327 px wide, so the outro rebuilds it as vector: the
fleur-de-lis is redrawn in SVG and the name is set in Cormorant Garamond to
match. Swap in a high-res logo if the firm has one.

**Bar notice:** the outro carries *FREE BACKGROUND INFORMATION AVAILABLE UPON
REQUEST* and *Oxford, Mississippi*, as laid out in the proposal. Still needed:
the name of the attorney responsible for the ad.

**Photos:** `assets/attorneys_source.jpg` (cropped to `attorneys_crop.jpg` for
the half-frame) and `assets/stan_little_source.webp` (Stan Little's headshot,
cropped to `stan_little_crop.jpg`; the source is only 1002×602, so it is used as
a small round portrait to stay sharp).

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
