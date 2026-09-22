# SOCSD 30-second ad (1920x1080)

`SOCSD_30s_1920x1080.mp4` — 30 s, 1920x1080, 30 fps, H.264 + AAC, ready for MCTV screens.
`SOCSD_keyframes.png` — one still from each scene for quick review.

## Add the real photos, logo, and music
Drop files into `assets/` (all optional), then re-render:

| File | Used for |
|------|----------|
| `scene1.jpg` … `scene5.jpg` | Photo behind each of the five copy scenes (slow zoom applied) |
| `logo.png` | District logo on the end card (transparent PNG) |
| `music.mp3` or `music.wav` | Background track, auto-trimmed to 30 s with fades |

```bash
pip install pillow numpy imageio-ffmpeg
cd ads/starkville-socsd/build
python3 render.py
```

Copy for each scene is in the `SCENES` list at the top of `build/render.py`.
