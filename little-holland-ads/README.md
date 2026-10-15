# Little & Holland PLLC — :15 spots for MCTV

| # | Spot | Audience | Status |
|---|------|----------|--------|
| 1 | `ad1-dui-students` — "Arrested for DUI? Let's talk." | College students | Draft v6 |
| 2 | Parents spot | Parents of college students | Not started |

## Spot 1 — storyboard (15 s, 1920×1080, 30 fps, silent)

| Time | Beat |
|------|------|
| 0.0–4.2 s | Police-light footage (`assets/police_lights_intro.mp4`) under a navy tint → *ARRESTED FOR* → **DUI?** (ivory serif, gold “?”) slams in with a camera shake → logo band rises from the bottom (solid navy, gold edge, fleur glint and sheen) → *Let's talk.* in gold italic |
| 3.75–8.3 s | Split screen: the attorneys' photo wipes in on the left behind a glowing gold edge; on the right, *You're an adult.* (gold italic) / **What you tell us** (ivory) / **stays between us.** (gold) → gold lock clicks shut: PRIVATE & CONFIDENTIAL |
| 8.2–10.6 s | Gold ring draws around Stan Little's portrait (*STAN LITTLE, ATTORNEY*) → **CALL LITTLE & HOLLAND** / **662.232.9500** (digits drop in) |
| 10.6–15.0 s | Call slide blurs away → the firm's homepage hero photo (the 1013 East Jackson Avenue office at sunset) fades up full screen → the website's navy veil settles over it and the photo softens slightly out of focus as the logo outro builds: gold fleur-de-lis grows up, *LITTLE & HOLLAND, PLLC* resolves letter by letter, *CONCIERGE ATTORNEYS* → contact block styled after the firm's website: **(662) 232-9500** (Cormorant Garamond, old-style figures, gold line phone icon), *1013 East Jackson Avenue, Oxford, Mississippi 38655* (gold pin icon), office hours line, *In Mississippi's oldest law office, circa 1893.* in gold italic, Bar notice line, light sheen across the name |

All on-screen type follows the firm's branding to match the outro: Cormorant
Garamond (the logo's serif) in ivory and gold on navy, with Montserrat for the
phone number and small caps lines. Police lights appear only in the intro
footage; the split-screen and call slides sit on the brand navy background, and
the outro sits on the homepage photo under the website's navy veil.

The intro footage pulses about 2.5 times a second, under the 3-per-second
photosensitivity guideline for public screens; the navy tint also roughly
halves the brightness swing.

The renderer can't decode H.264 in headless Chromium, so `ad1-dui-students/prepare.sh`
(run automatically by `render.cjs`) extracts the footage to stills in `.work/footage/`.

**Outro photo:** `assets/home_hero_building_source.webp` (the homepage hero image,
1774×887) is cropped to 16:9 and resized to `assets/home_hero_building.jpg`.

**Logo:** the firm's logo file (`assets/little_holland_logo_reference.png`, from
the proposal) is only 327 px wide, so the outro rebuilds it as vector: the
fleur-de-lis is redrawn in SVG and the name is set in Cormorant Garamond to
match. Swap in a high-res logo if the firm has one.

**Bar notice:** the outro carries *FREE BACKGROUND INFORMATION AVAILABLE UPON
REQUEST* and the office address in Oxford, Mississippi, as laid out in the proposal. Still needed:
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

Requires `ffmpeg`. Fonts (Montserrat, Cormorant Garamond — SIL OFL)
are in `fonts/`.
