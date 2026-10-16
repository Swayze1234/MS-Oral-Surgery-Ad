# Oxford Christmas Galleria · 30-second MCTV ad + director one-pager

Silent 30-second digital ad (1920×1080, MP4) for the Oxford Christmas Galleria
(Sat Nov 28, 2026, 9 AM – 4:30 PM, 365 MS 6, Oxford MS 38655), plus a one-page
campaign proposal for the event director.

## Deliverables (`output/`)
| File | What it is |
|---|---|
| `OCG_30s_1920x1080_MCTV.mp4` | The ad at MCTV screen spec (H.264, 30 fps, ~640 kb/s, no audio). Upload this one. |
| `OCG_30s_1920x1080_master.mp4` | Same ad, high-quality master (for social or re-encoding). |
| `OCG_MCTV_One_Pager.pdf` | One-page proposal: event, storyboard, where it runs, spotlight calendar, pricing, timeline. |
| `OCG_30s_filmstrip.jpg` | One frame per second of the finished ad, for a quick review. |
| `stills/` | Key frames used in the one-pager storyboard. |

## Ad structure
| Time | Scene |
|---|---|
| 0–4 s | Logo intro: cream disc lands on a kraft table, cut-paper sprigs set down one pair at a time, berries pop, "Oxford" stamps down with one bounce, the red dots flick out from under it, "Christmas Galleria" sets in glyph by glyph, then we fly through the wreath into the next scene. |
| 4–9 s | Save the date: Saturday · Nov. 28 · 9 AM – 4:30 PM · address, with last year's banner photo. |
| 9–14 s | "50+" counts up; three polaroids of last year drop in. |
| 14–23 s | Three featured artists, 3 s each (photo, name, medium, handle). |
| 23–27 s | "Consider your Christmas shopping handled." |
| 27–30 s | End card: logo, date, time, address, 50+ artists. |

## Swapping in the real artists
Edit `ad/artists.json` (name, medium, handle, photo path, optional `focus` for the
photo crop), drop the photos into `assets/photos/`, then rebuild (below).
Three to five artists fit the 9-second slot; the per-artist time adapts automatically.

## Rebuilding
```bash
pip install pillow imageio-ffmpeg pymupdf "playwright==1.56.0"
python3 -m playwright install chromium            # one-time browser download
cd assets/logo && python3 make_logo.py          # vector wreath logo (logo.svg + fragment)
cd ../../ad && python3 build.py                  # assembles ad/index.html
python3 render.py --stills                       # renders 900 frames -> output/*.mp4 (+ key stills)
cd ../one-pager && python3 build_pdf.py          # one-pager PDF
```
`render.py --preview` renders a fast 10-fps check; `--only-stills` just refreshes the key frames.

The ad is plain HTML/CSS/SVG driven by a deterministic `render(t)` function
(`ad/template.html` for the scenes, `ad/logo_timeline.js` for the logo intro),
captured frame by frame with headless Chromium and encoded with ffmpeg.

## Assets
- `assets/logo/` — the original 540 px logo and the vector rebuild used on screen.
- `assets/photos/` — last year's event photos supplied by the client.
- `assets/fonts/` — Pacifico, Bree Serif, Playfair Display, Montserrat (Google Fonts, OFL).
