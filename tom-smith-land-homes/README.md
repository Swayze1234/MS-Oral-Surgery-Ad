# Tom Smith Land & Homes — 30-second digital ad

`output/Tom_Smith_Land_Homes_30s.mp4` is a silent, 30-second, 1920×1080 (16:9)
H.264 spot built to the MCTV Digital ad spec (MP4, 300–700 kb/s, under 20 MB).

## Storyboard

| Time | Slide | What happens |
|------|-------|--------------|
| 0–7 s | Intro | Green wave + blue band rise in. The logo builds itself in the center of the frame: roof draws on, chimney appears, "Tom" and "Smith" pop in, the two pines grow up, then "LAND AND HOMES" and "Expect More. Get More." rise in. Website fades in on the band. |
| 7–18 s | Chance Persac | Logo glides to the right (larger than the name). Chance's cut-out headshot rises on the left over the band, business-card style. "CHANCE / PERSAC / REALTOR®", "Office phone: 662.268.6333", "Cell phone: (601) 955-4587" slide in. Band headline: "LAND OR HOME? / GET THE BEST OF BOTH WORLDS." |
| 18.7–30 s | Brady Richardson | Logo glides to the top-left. Brady's cut-out headshot rises on the right. "BRADY / RICHARDSON" (larger than Chance's name) slides in. Band headline: "YOUR LOCAL / HOMETOWN REALTORS". |

The website `TomSmithLandandHomes.com` (from the business card) sits in the blue
band on every slide.

## Files

- `ad.html` — the whole ad: layout, vector logo and all CSS animations. Open it in
  a browser to preview it playing in real time (it is sized to 1920×1080).
- `render.js` — seeks the page's animations frame by frame with Playwright and
  pipes the frames to ffmpeg. Deterministic output.
- `prepare_headshots.py` — upscales the two headshots and removes their
  backgrounds (rembg) to produce `assets/img/*-cutout.png`.
- `assets/fonts/` — Montserrat (name/phone text, as on the card), Ultra (logo
  wordmark), Liberation Serif (LAND AND HOMES, tagline, band headlines).
- `assets/source/` — the original business card and headshots supplied.

## Notes

- The original logo SVG was not included in the upload, so the mark was rebuilt
  as vector art from the business card (colors sampled from it). Swap in the real
  SVG by replacing the `LOGO` template in `ad.html` if you have it.
- Brady's headshot was supplied at 375×450 px and is upscaled 2.6× for 1080p, so it
  is a little softer than Chance's. A larger original will drop straight in.

## Rebuild

```bash
pip install pillow rembg onnxruntime imageio-ffmpeg   # imageio-ffmpeg bundles ffmpeg
python3 prepare_headshots.py                          # only if headshots change
NODE_PATH=/opt/node22/lib/node_modules \
FFMPEG=$(python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())") \
node render.js                                        # writes output/Tom_Smith_Land_Homes_30s.mp4

STILLS=4,12,24 node render.js                         # preview PNGs instead of the video
```
