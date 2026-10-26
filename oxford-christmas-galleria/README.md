# Oxford Christmas Galleria · 30-second MCTV ad + director one-pager

Silent 30-second digital ad (1920×1080, MP4) for the Oxford Christmas Galleria
(Sat Nov 28, 2026, 9 AM – 4 PM, The Jefferson, 365 MS 6, Oxford MS 38655; free
admission, free parking, tote bags for the first 100 shoppers), plus a one-page
campaign proposal for the event director.

## Deliverables (`output/`)
| File | What it is |
|---|---|
| `OCG_30s_1920x1080_MCTV.mp4` | The ad at MCTV screen spec (H.264, 30 fps, ~640 kb/s, no audio). Upload this one. |
| `OCG_30s_1920x1080_master.mp4` | Same ad, high-quality master (for social or re-encoding). |
| `OCG_MCTV_One_Pager.pdf` | One-page proposal: event, storyboard, where it runs, on-screen copy, pricing, timeline. |
| `OCG_30s_filmstrip.jpg` | One frame per second of the finished ad, for a quick review. |
| `OCG_MCTV_One_Pager_preview.png` | PNG preview of the one-pager. |
| `stills/` | Key frames used in the one-pager storyboard. |

## Ad structure
| Time | Scene |
|---|---|
| 0–4 s | Logo intro: a cream card lands on a kraft table, the OXFORD letters are set down one by one, "Christmas" is written on with a gold pen tip, the tree pops onto the i, the GALLERIA letters set in, a short hold with foil-star twinkles, then the card grows to hand off to the next scene. |
| 4–9 s | Save the date: Saturday · Nov. 28 · 9 AM – 4 PM · The Jefferson, with last year's banner photo. |
| 9–14 s | "50+" counts up; three polaroids of last year drop in. |
| 14–23 s | Two perk beats, 4.5 s each: "Free admission / Free parking", then "First 100 shoppers get a free OCG tote bag". Each beat has a photo or video slot. |
| 23–27 s | "Consider your Christmas shopping handled." |
| 27–30 s | End card: wordmark, date, time, The Jefferson, 50+ artists, free admission and parking. |

An MCTV wordmark bug (`assets/logo/mctv-wordmark-green.png`, from the media kit) sits bottom-right on every frame.

## Swapping in photos or video
`ad/media.json` lists the two media slots used at 14–23 s. Each entry is either

- an image: `{"type":"image","src":"../assets/photos/x.jpg","focus":"50% 40%"}` (slow Ken Burns zoom), or
- a video clip as a folder of JPEG frames: `{"type":"video","frames":"../assets/video/clip1","count":135,"fps":30,"focus":[0.5,0.5]}`.

The current cut uses last year's Facebook reel (`assets/video/reel-2025.mp4`, 720×1280).
`assets/video/extract_clips.py` cuts it into the two frame folders (`clipA`, `clipB`, 135
frames each; the segments are listed at the top of the script). The frame folders are not
committed, so run the script once before rendering:

```bash
python3 assets/video/extract_clips.py
```

Vertical footage is drawn sharp at full height with a blurred fill at the sides; landscape
footage is cover-cropped. The scene-3 polaroids and the scene-2 photo are set directly in
`ad/template.html`.

## Rebuilding
```bash
pip install pillow numpy scipy imageio-ffmpeg pymupdf "playwright==1.56.0"
python3 -m playwright install chromium            # one-time browser download
python3 assets/video/extract_clips.py            # frame folders for the two footage slots
cd ad && python3 build.py                        # assembles ad/index.html from the template + logo slices + media.json
python3 render.py --stills                       # renders 900 frames -> output/*.mp4 (+ key stills)
cd ../one-pager && python3 build_pdf.py          # one-pager PDF
```
`render.py --preview` renders a fast 10-fps check; `--only-stills` just refreshes the key frames.

The ad is plain HTML/CSS driven by a deterministic `render(t)` function
(`ad/template.html` for the scenes, `ad/logo_timeline.js` for the logo intro),
captured frame by frame with headless Chromium and encoded with ffmpeg.

### Logo
`assets/logo/wordmark-original-1200.jpg` is the client's logo. `assets/logo/ocg-wordmark.png`
is the same wordmark cut out with transparency, and `assets/logo/slices/` holds it split into
16 pieces (6 OXFORD letters, the script, the tree, 8 GALLERIA letters) plus `manifest.json`
with their positions; the intro animates those pieces. A larger PNG or vector master of the
logo would sharpen the intro slightly; drop it in as `wordmark-original-1200.jpg` and re-run `python3 slice_wordmark.py`.
The earlier wreath rebuild (`make_logo.py`, `logo.svg`) is kept for reference only.

## Assets
- `assets/logo/` — the client's wordmark (JPG), its transparent cutout and animation slices, plus the earlier wreath logo for reference.
- `assets/photos/` — last year's event photos supplied by the client.
- `assets/fonts/` — Pacifico, Bree Serif, Playfair Display, Montserrat (Google Fonts, OFL).
