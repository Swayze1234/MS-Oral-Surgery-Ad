# Tom Smith Land & Homes — 30-second digital ad

`output/Tom_Smith_Land_Homes_30s.mp4` is a silent, 30-second, 1920×1080 (16:9)
H.264 spot built to the MCTV Digital ad spec (MP4, 300–700 kb/s, under 20 MB).

## Storyboard

| Time | Slide | What happens |
|------|-------|--------------|
| 0–7 s | Intro | Green wave + blue band rise in. The logo builds itself in the center of the frame: roof wipes on, "Tom" and "Smith" pop in, the two pines grow up out of the lettering, then "LAND AND HOMES" and "Expect More. Get More." rise in. Website fades in on the band. |
| 7–18 s | Chance Persac | Logo glides to the right (larger than the name). Chance's cut-out headshot rises on the left over the band, business-card style. "CHANCE / PERSAC / REALTOR®", "Office phone: 662.268.6333", "Cell phone: (601) 955-4587" slide in. Band headline: "LAND OR HOME? / GET THE BEST OF BOTH WORLDS." |
| 18.7–30 s | Brady Richardson | Logo glides to the top-left at near full size (the largest element on the slide). Brady's cut-out headshot rises on the right. "YOUR LOCAL / HOMETOWN / REALTORS" and the website sit beside the logo. In the blue band: "BRADY / RICHARDSON" in white (larger than Chance's name), then "Office Phone (662) 268-6333" and "Mobile (662) 418-8791". |

The website `TomSmithLandandHomes.com` (from the business card) appears on every
slide.

## Files

- `ad.html` — the whole ad: layout, logo layers and all CSS animations. Open it in
  a browser to preview it playing in real time (it is sized to 1920×1080).
- `render.js` — seeks the page's animations frame by frame with Playwright and
  pipes the frames to ffmpeg. Deterministic output.
- `prepare_headshots.py` — upscales the two headshots and removes their
  backgrounds (rembg) to produce `assets/img/*-cutout.png`.
- `prepare_logo.py` — takes the supplied logo (`assets/source/tom-smith-logo.jpg`),
  removes the green circle and the white background, upscales it 4×, and cuts it
  into the seven layers in `assets/img/logo/` (roof, Tom, Smith, trees, LAND AND,
  HOMES, tagline) that the intro animates one by one. `layers.js` holds their
  positions.
- `assets/fonts/` — Montserrat (name/phone text, as on the card) and Liberation
  Serif (band headlines).
- `assets/img/background.jpg` — the supplied park bokeh photo, cropped to 16:9 and
  scaled to 1920×1080. `ad.html` lays a light white wash over it so the navy
  type and the green parts of the logo stay legible, and gives the logo pieces a
  soft white halo.
- `assets/source/` — the original logo, background, business card and headshots supplied.

## Notes

- The logo was supplied as a 500×500 JPEG with a green circle around it. The
  circle is removed and the artwork is upscaled 4× for 1080p. A larger or vector
  original would sharpen it further: drop it in as `assets/source/tom-smith-logo.jpg`
  (or adjust `SRC` in `prepare_logo.py`) and re-run the script.
- In the intro the pines grow up out of the "Smith" lettering: the white keyline
  between the letters and the trees is too thin in the 500 px file to separate
  them any other way, so the green artwork is split at the letters' cap line.
- Brady's headshot was supplied at 375×450 px and is upscaled 2.6× for 1080p, so it
  is a little softer than Chance's. A larger original will drop straight in.

## Rebuild

```bash
# background (only if the photo changes): crop to 16:9 and scale to 1920x1080
python3 -c "from PIL import Image,ImageFilter; im=Image.open('assets/source/park-bokeh.webp').convert('RGB'); w,h=im.size; th=round(w*9/16); t=(h-th)//2; im.crop((0,t,w,t+th)).resize((1920,1080),Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5)).save('assets/img/background.jpg',quality=90)"
pip install pillow numpy scipy rembg onnxruntime imageio-ffmpeg   # imageio-ffmpeg bundles ffmpeg
python3 prepare_headshots.py                          # only if headshots change
python3 prepare_logo.py                               # only if the logo changes
NODE_PATH=/opt/node22/lib/node_modules \
FFMPEG=$(python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())") \
node render.js                                        # writes output/Tom_Smith_Land_Homes_30s.mp4

STILLS=4,12,24 node render.js                         # preview PNGs instead of the video
```
