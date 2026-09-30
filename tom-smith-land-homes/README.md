# Tom Smith Land & Homes — 30-second digital ad

`output/Tom_Smith_Land_Homes_30s.mp4` is a silent, 30-second, 1920×1080 (16:9)
H.264 spot built to the MCTV Digital ad spec (MP4, 300–700 kb/s, under 20 MB).

## Storyboard

| Time | Slide | What happens |
|------|-------|--------------|
| 0–6.4 s | Intro | Green wave + blue band rise in. The logo builds itself in the center of the frame: the roof appears (wipes on left to right), the two pines rise one after the other, then "Tom", "Smith", "LAND AND", "HOMES" and "Expect More. Get More." drop in from above. Website fades in on the band, a light sweeps across the logo, and the logo pulses just before the transition. |
| 6.4–7.9 s | Transition | A green-edged blue wave, slightly tilted, sweeps up through the whole frame. While it covers the screen the logo jumps to its slide-2 spot; the wave's trailing edge then uncovers Chance's slide from the bottom up. |
| 7.3–22.4 s | Chance Persac | Chance's cut-out headshot rises on the left over the band, business-card style. "CHANCE / PERSAC / REALTOR®", "Office phone: (662)268-6333", "Cell phone: (601) 955-4587" slide in. The logo sits on the right, larger than the name. Band headline: "LAND OR HOME? / GET THE BEST OF BOTH WORLDS." |
| 22.4–23.9 s | Transition | The same wave sweeps down from the top. While covered, Chance's slide hides and the logo jumps back to the center. |
| 23.3–30 s | Outro | Logo large in the center. In the band: "TomSmithLandandHomes.com" and "Call (662)268-6333" rise in; a light sweeps across the logo once more. |

The website `TomSmithLandandHomes.com` (from the business card) appears on every
slide.

## Files

- `ad.html` — the whole ad: layout, logo layers and all CSS animations. Open it in
  a browser to preview it playing in real time (it is sized to 1920×1080).
- `render.js` — seeks the page's animations frame by frame with Playwright and
  pipes the frames to ffmpeg. Deterministic output.
- `prepare_headshots.py` — upscales Chance's headshot and removes its
  background (rembg) to produce `assets/img/chance-cutout.png`.
- `prepare_logo.py` — takes the supplied logo (`assets/source/tom-smith-logo.jpg`),
  removes the green circle and the white background, upscales it 4×, and cuts it
  into the eight layers in `assets/img/logo/` (roof, the two pines, Tom, Smith,
  LAND AND, HOMES, tagline) that the intro animates one by one. `layers.js` holds
  their positions and draw order.
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
- The pines' trunks end behind the "Smith" lettering in the artwork, and the
  white keyline between letters and trees is too thin in the 500 px file to
  separate them by colour. The green artwork is therefore split at the letters'
  cap line, and each pine gets a short tapered trunk drawn down to the letters'
  baseline so it is a complete shape while it rises; the letters then drop on
  top and hide the join.
- Brady Richardson's slide was removed at the client's request; his source photo
  is kept in `assets/source/` in case it is wanted again.

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

STILLS=2,5,12,26 node render.js                       # preview PNGs instead of the video
```
